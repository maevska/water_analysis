import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from catboost import CatBoostClassifier

SEQUENCE_LENGTH = 10
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
FEATURES = ['temp_water', 'temp_air', 'precipitation', 'water_level', 'pH', 'turbidity', 'oxygen', 'nitrates', 'ammonia']
TARGETS = ['turbidity', 'oxygen', 'water_level']
CATBOOST_FEATURES = ['oxygen', 'pH', 'nitrates', 'ammonia', 'precipitation', 'water_level', 'turbidity']

LABEL_MAPPING = {
    'clean': 'Чистая вода',
    'medium': 'Среднее качество воды',
    'bad': 'Плохое качество воды'
}

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.fc(out)
        return out

def get_user_input():
    print('\nВведите значения признаков через пробел в следующем порядке:')
    print(', '.join(FEATURES))
    print('Пример: 15.0 20.0 0.5 3.2 7.0 8.0 8.1 2.5 0.1')

    while True:
        try:
            user_input = input('\nВаш ввод: ').strip()
            if not user_input:
                print("Используем пример: 15.0 20.0 0.5 3.2 7.0 8.0 8.1 2.5 0.1")
                user_input = "15.0 20.0 0.5 3.2 7.0 8.0 8.1 2.5 0.1"
            
            values = [float(x) for x in user_input.split()]
            if len(values) != len(FEATURES):
                print(f'❗ Нужно ввести ровно {len(FEATURES)} чисел. Попробуйте снова.')
                continue
            return values
        except ValueError:
            print('❗ Ошибка ввода. Убедитесь, что вводите только числа, разделённые пробелами.')

def prepare_lstm_input(input_values, scaler_X):
    single_data_scaled = scaler_X.transform([input_values])
    sequence = np.array([single_data_scaled[0]] * SEQUENCE_LENGTH)
    sequence = torch.tensor(sequence, dtype=torch.float32).unsqueeze(0).to(DEVICE)
    return sequence

def prepare_catboost_input(input_values):
    feature_indices = [FEATURES.index(f) for f in CATBOOST_FEATURES]
    catboost_input = [input_values[i] for i in feature_indices]
    return np.array([catboost_input])

def plot_results(input_values, predictions):
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
    plt.show() 
    # plt.savefig('lstm_predictions.png') 
    plt.close() 

def predict():
    df_train = pd.read_csv('diplom-project/models_for_water-main/datasets/water_quality_dataset.csv')
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()
    scaler_X.fit(df_train[FEATURES].values)
    scaler_y.fit(df_train[TARGETS].values)

    input_values = get_user_input()

    lstm_input = prepare_lstm_input(input_values, scaler_X)
    lstm_model = LSTMModel(input_size=len(FEATURES), hidden_size=64, num_layers=2, output_size=len(TARGETS)).to(DEVICE)
    lstm_model.load_state_dict(torch.load('diplom-project/models_for_water-main/models/lstm_multitask_water_quality_model.pth', map_location=DEVICE))
    lstm_model.eval()

    with torch.no_grad():
        lstm_prediction = lstm_model(lstm_input)
    lstm_prediction = lstm_prediction.cpu().numpy()
    lstm_prediction_original = scaler_y.inverse_transform(lstm_prediction)[0]

    catboost_input = prepare_catboost_input(input_values)

    catboost_model = CatBoostClassifier()
    catboost_model.load_model('diplom-project/models_for_water-main/models/water_catboost_model.cbm')
    catboost_prediction = catboost_model.predict(catboost_input)[0][0] 
    
    print('\nПредсказание гидробиологических показателей:')
    for target_name, value in zip(TARGETS, lstm_prediction_original):
        print(f'{target_name}: {value:.3f}')

    print('\nОценка качества воды:')
    print(f'Класс: {LABEL_MAPPING[catboost_prediction]}')
    
    plot_results(input_values, lstm_prediction_original)

if __name__ == '__main__':
    predict()