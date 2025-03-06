import numpy as np
from sklearn.metrics import f1_score
import pandas as pd  # Добавьте импорт pandas


def calculate_f1_score(true_intervals, pred_intervals, data, time_tolerance=0.08333):
    # Преобразуем интервалы в бинарные метки
    true_labels = np.zeros(len(data))
    pred_labels = np.zeros(len(data))

    for interval in true_intervals:
        start_idx = np.searchsorted(data["Время (часы)"], interval[0] - time_tolerance)
        end_idx = np.searchsorted(data["Время (часы)"], interval[1] + time_tolerance)
        true_labels[start_idx:end_idx] = 1

    for interval in pred_intervals:
        start_idx = np.searchsorted(data["Время (часы)"], interval[0] - time_tolerance)
        end_idx = np.searchsorted(data["Время (часы)"], interval[1] + time_tolerance)
        pred_labels[start_idx:end_idx] = 1

    return f1_score(true_labels, pred_labels)


if __name__ == "__main__":
    # Пример данных
    data = pd.DataFrame({
        "Время (часы)": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Давление (атм)": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150]
    })

    # Пример интервалов
    true_recovery = [[1, 3]]  # Пример эталонных интервалов
    true_drop = [[5, 7]]
    recovery_intervals = [[1, 3]]  # Пример предсказанных интервалов
    drop_intervals = [[5, 7]]  # Пример предсказанных интервалов

    # Оценка качества
    f1_recovery = calculate_f1_score(true_recovery, recovery_intervals, data)
    f1_drop = calculate_f1_score(true_drop, drop_intervals, data)

    print("F1-score для КВД:", f1_recovery)
    print("F1-score для КПД:", f1_drop)