import numpy as np
from sklearn.metrics import f1_score

def calculate_f1_score(true_intervals, pred_intervals, data, time_tolerance=0.08333):
    """
    Вычисляет F1-score на основе эталонных и предсказанных интервалов.

    Параметры:
        true_intervals (list): Эталонные интервалы в формате [[start1, end1], [start2, end2], ...].
        pred_intervals (list): Предсказанные интервалы в формате [[start1, end1], [start2, end2], ...].
        data (pd.DataFrame): Данные с колонками "Время (часы)" и "Давление (атм)".
        time_tolerance (float): Допуск по времени для сравнения интервалов (по умолчанию 0.08333 часа = 5 минут).

    Возвращает:
        float: F1-score.
    """
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