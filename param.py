from sklearn.model_selection import ParameterGrid
from search import detect_patterns
from f1score import calculate_f1_score
import pandas as pd
import os

# Загрузка реальных данных
def load_real_data():
    """
    Загружает реальные данные для тестирования.

    Возвращает:
        tuple: (real_data, true_recovery, true_drop) - данные и эталонные интервалы.
    """
    # Загрузка данных
    real_data = pd.read_csv(os.path.join("data", "real_well_data.csv"))
    real_data.columns = ["Время (часы)", "Давление (атм)"]

    # Загрузка эталонной разметки
    true_intervals = pd.read_csv(os.path.join("true_intervals", "real_well_data.csv"))
    true_recovery = eval(true_intervals["recovery"].iloc[0])
    true_drop = eval(true_intervals["drop"].iloc[0])

    return real_data, true_recovery, true_drop

# Определяем диапазоны параметров
param_grid = {
    'window_size': [5, 10, 15],
    'threshold': [3.0, 5.0, 7.0],
    'noise_threshold': [5.0, 10.0, 15.0]
}

# Функция для оценки качества при разных параметрах
def evaluate_parameters(data, true_recovery, true_drop, params):
    """
    Оценивает качество алгоритма при заданных параметрах.

    Параметры:
        data (pd.DataFrame): Данные с колонками "Время (часы)" и "Давление (атм)".
        true_recovery (list): Эталонные интервалы КВД.
        true_drop (list): Эталонные интервалы КПД.
        params (dict): Параметры для алгоритма.

    Возвращает:
        float: Средний F1-score.
    """
    recovery_intervals, drop_intervals = detect_patterns(data, **params)
    f1_recovery = calculate_f1_score(true_recovery, recovery_intervals, data)
    f1_drop = calculate_f1_score(true_drop, drop_intervals, data)
    return (f1_recovery + f1_drop) / 2  # Средний F1-score

# Загрузка реальных данных
real_data, true_recovery, true_drop = load_real_data()

# Поиск оптимальных параметров
best_score = 0
best_params = {}
for params in ParameterGrid(param_grid):
    score = evaluate_parameters(real_data, true_recovery, true_drop, params)
    if score > best_score:
        best_score = score
        best_params = params

print("Лучшие параметры:", best_params)
print("Лучший F1-score:", best_score)