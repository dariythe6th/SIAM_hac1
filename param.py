from sklearn.model_selection import ParameterGrid
import numpy as np
import pandas as pd
from search import detect_patterns
from f1score import calculate_f1_score
from utils import safe_parse_intervals

def evaluate_parameters(data, true_recovery, true_drop, params):
    """
    Оценивает качество алгоритма (средний F1-score) для заданных параметров.
    """
    recovery_intervals, drop_intervals = detect_patterns(data, **params)
    f1_recovery = calculate_f1_score(true_recovery, recovery_intervals, data)
    f1_drop = calculate_f1_score(true_drop, drop_intervals, data)
    return (f1_recovery + f1_drop) / 2

# Загрузка данных для подбора параметров
real_data = pd.read_csv("real_well_data.csv")
real_data.columns = ["Время (часы)", "Давление (атм)"]

true_intervals = pd.read_csv("true_intervals.csv")
true_recovery = safe_parse_intervals(true_intervals["recovery"].iloc[0])
true_drop = safe_parse_intervals(true_intervals["drop"].iloc[0])

# Определение диапазонов параметров
param_grid = {
    'window_size': [5, 10, 15],
    'threshold': [3.0, 5.0, 7.0],
    'min_points': [20],
    'noise_threshold': [5.0, 10.0, 15.0],
    'min_recovery_duration': [4],
    'min_drop_duration': [6],
    'low_density_threshold': [10]
}

best_score = 0
best_params = {}
for params in ParameterGrid(param_grid):
    score = evaluate_parameters(real_data, true_recovery, true_drop, params)
    if score > best_score:
        best_score = score
        best_params = params

print("Лучшие параметры:", best_params)
print("Лучший F1-score:", best_score)
