import sys
from pathlib import Path
import numpy as np
import torch
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict, Tuple
from catboost import CatBoostClassifier
from app.core.config import settings
from app.core.exceptions import WaterQualityException

testing_path = Path(__file__).parent.parent.parent.parent / 'models_for_water-main' / 'test_models'
sys.path.append(str(testing_path))

from testing import (
    FEATURES,
    TARGETS,
    LSTMModel,
    DEVICE,
    prepare_lstm_input,
    prepare_catboost_input
)

LABEL_MAPPING = {
    'good': 'Хорошее качество воды',
    'medium': 'Среднее качество воды',
    'bad': 'Плохое качество воды'
}

class MLService:
    def __init__(self):
        self._initialize_scalers()
        self._load_models()

    def _initialize_scalers(self):
        try:
            dataset_path = Path(settings.DATASETS_DIR) / 'water_quality_dataset.csv'
            df_train = pd.read_csv(dataset_path)
            
            self.scaler_X = MinMaxScaler()
            self.scaler_y = MinMaxScaler()
            
            self.scaler_X.fit(df_train[FEATURES].values)
            self.scaler_y.fit(df_train[TARGETS].values)
        except Exception as e:
            raise WaterQualityException(
                status_code=500,
                detail=f"Ошибка при инициализации скейлеров: {str(e)}"
            )

    def _load_models(self):
        try:
            models_path = Path(settings.MODELS_DIR)
            

            self.lstm_model = LSTMModel(
                input_size=len(FEATURES),
                hidden_size=64,
                num_layers=2,
                output_size=len(TARGETS)
            ).to(DEVICE)
            
            self.lstm_model.load_state_dict(torch.load(
                models_path / 'lstm_multitask_water_quality_model.pth',
                map_location=DEVICE
            ))
            self.lstm_model.eval()

            self.catboost_model = CatBoostClassifier()
            self.catboost_model.load_model(models_path / 'water_catboost_model.cbm')
        except Exception as e:
            raise WaterQualityException(
                status_code=500,
                detail=f"Ошибка загрузки моделей: {str(e)}"
            )

    def _plot_results_to_base64(self, input_values: List[float], predictions: List[float]) -> str:
        try:
            plt.figure(figsize=(12, 8))
            target_indices = [FEATURES.index(target) for target in TARGETS]
            input_targets = [input_values[i] for i in target_indices]
            x = np.arange(len(TARGETS))
            width = 0.35

            plt.bar(x - width/2, input_targets, width, label='Текущие показатели', color='blue')
            plt.bar(x + width/2, predictions, width, label='Предсказанные показатели', color='orange')

            plt.xlabel('Параметры')
            plt.ylabel('Значения')
            plt.xticks(x, TARGETS)
            plt.legend()
            plt.grid(True)

            for i, (inp, pred) in enumerate(zip(input_targets, predictions)):
                plt.text(i - width/2, inp + 0.05, f'{inp:.2f}', ha='center')
                plt.text(i + width/2, pred + 0.05, f'{pred:.2f}', ha='center')

            plt.tight_layout()
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            return base64.b64encode(buf.read()).decode('utf-8')
        except Exception as e:
            raise WaterQualityException(
                status_code=500,
                detail=f"Ошибка при создании графика: {str(e)}"
            )

    def predict(self, parameters: Dict[str, float]) -> Tuple[Dict[str, float], str, str]:
        try:
            input_values = []
            for feature in FEATURES:
                feature_lower = feature.lower() if feature != 'pH' else 'ph'
                if feature_lower not in parameters:
                    raise WaterQualityException(
                        status_code=400,
                        detail=f"Отсутствует параметр: {feature}"
                    )
                input_values.append(float(parameters[feature_lower]))

            with torch.no_grad():
                lstm_input = prepare_lstm_input(input_values, self.scaler_X)
                lstm_prediction = self.lstm_model(lstm_input)
                lstm_prediction = lstm_prediction.cpu().numpy()[0]
                lstm_prediction = self.scaler_y.inverse_transform([lstm_prediction])[0]
                lstm_prediction = [float(x) for x in lstm_prediction]

            catboost_input = prepare_catboost_input(input_values)
            water_quality_class = self.catboost_model.predict(catboost_input)[0]
            water_quality_class = str(water_quality_class[0] if isinstance(water_quality_class, (list, np.ndarray)) else water_quality_class)
            
            if water_quality_class not in LABEL_MAPPING:
                raise ValueError(f"Неизвестный класс качества воды: {water_quality_class}")

            predictions = {
                target: pred 
                for target, pred in zip(TARGETS, lstm_prediction)
            }

            plot_data = self._plot_results_to_base64(input_values, lstm_prediction)

            return predictions, water_quality_class, plot_data

        except Exception as e:
            if isinstance(e, WaterQualityException):
                raise e
            raise WaterQualityException(
                status_code=500,
                detail=f"Ошибка при получении предсказаний: {str(e)}"
            ) 