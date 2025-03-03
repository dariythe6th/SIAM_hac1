from sklearn.model_selection import ParameterGrid

# Определяем диапазоны параметров
param_grid = {
    'window_size': [5, 10, 15],
    'threshold': [3.0, 5.0, 7.0],
    'noise_threshold': [5.0, 10.0, 15.0]
}

# Функция для оценки качества при разных параметрах
def evaluate_parameters(data, true_recovery, true_drop, params):
    recovery_intervals, drop_intervals = detect_patterns(data, **params)
    f1_recovery = calculate_f1_score(true_recovery, recovery_intervals)
    f1_drop = calculate_f1_score(true_drop, drop_intervals)
    return (f1_recovery + f1_drop) / 2  # Средний F1-score

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