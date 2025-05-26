import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

SEQUENCE_LENGTH = 10
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

features = ['temp_water', 'temp_air', 'precipitation', 'water_level','pH','turbidity', 'oxygen', 'nitrates', 'ammonia']
targets = ['turbidity', 'oxygen', 'water_level'] 

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
    print('Введите значения признаков через запятую в следующем порядке:')
    print(', '.join(features))
    print('Пример: 15.0, 20.0, 0.5, 3.2, 7.0, 8.0, 0.3, 0.1')

    while True:
        try:
            user_input = input('\nВаш ввод: ')
            values = [float(x.strip()) for x in user_input.split(',')]
            if len(values) != len(features):
                print(f'❗ Нужно ввести ровно {len(features)} чисел. Попробуйте снова.')
                continue
            return values
        except ValueError:
            print('❗ Ошибка ввода. Убедитесь, что вводите только числа, разделённые запятыми.')
def plot_results(input_values, predictions):
    plt.figure(figsize=(12, 8))
    
    target_indices = [features.index(target) for target in targets]
    
    input_targets = [input_values[i] for i in target_indices]
    x = np.arange(len(targets))
    width = 0.35
    
    plt.bar(x - width/2, input_targets, width, label='Входные значения', color='blue')
    plt.bar(x + width/2, predictions, width, label='Предсказанные', color='orange')
    
    plt.xlabel('Параметры')
    plt.ylabel('Значения')
    plt.title('Сравнение входных и предсказанных значений')
    plt.xticks(x, targets)
    plt.legend()
    plt.grid(True)
    
    for i, (inp, pred) in enumerate(zip(input_targets, predictions)):
        plt.text(i - width/2, inp + 0.05, f'{inp:.2f}', ha='center')
        plt.text(i + width/2, pred + 0.05, f'{pred:.2f}', ha='center')
    
    plt.tight_layout()
    plt.show()

# Здесь нужно подшаманить, чтобы не было зависимости от train_loader
# и test_loader, которые используются только для обучения и тестирования модели, для этого нужно чтобы была основная программа, которая будет использоваться для предсказания
# и в ней будет использоваться модель, которая была обучена на train_loader и test_loader
def predict():

    single_data = get_user_input()

    import pandas as pd
    df_train = pd.read_csv('my-website-project/models_for_water-main/datasets/water_quality_dataset.csv')
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()
    scaler_X.fit(df_train[features].values)
    scaler_y.fit(df_train[targets].values)

    single_data_scaled = scaler_X.transform([single_data])

    sequence = np.array([single_data_scaled[0]] * SEQUENCE_LENGTH)
    sequence = torch.tensor(sequence, dtype=torch.float32).unsqueeze(0).to(DEVICE)

    model = LSTMModel(input_size=len(features), hidden_size=64, num_layers=2, output_size=len(targets)).to(DEVICE)
    model.load_state_dict(torch.load('my-website-project/models_for_water-main/models/lstm_multitask_water_quality_model.pth', map_location=DEVICE))
    model.eval()

    with torch.no_grad():
        prediction = model(sequence)

    prediction = prediction.cpu().numpy()
    prediction_original = scaler_y.inverse_transform(prediction)

    print('\n📈 Предсказание:')
    for target_name, value in zip(targets, prediction_original[0]):
        print(f'{target_name}: {value:.3f}')
    
    plot_results(single_data, prediction_original[0])

if __name__ == '__main__':
    predict()
