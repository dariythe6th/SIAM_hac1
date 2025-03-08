import numpy as np
import pandas as pd
from scipy.signal import savgol_filter


def check_point_density(data, start_idx, end_idx, min_points=20):
    """
    Проверяет, что в интервале имеется достаточное количество точек.
    Считает точки в первые 1 час (6 точек при 10-минутном интервале).
    """
    first_hour_end = start_idx + 6
    if first_hour_end > end_idx:
        return False
    return (end_idx - start_idx) >= min_points


def check_for_noise(data, start_idx, end_idx, noise_threshold=10.0):
    """
    Проверяет наличие резких скачков давления в интервале.
    Если разница между соседними точками превышает noise_threshold, интервал считается зашумленным.
    """
    pressure_diff = np.abs(np.diff(data["Давление (атм)"][start_idx:end_idx]))
    return np.any(pressure_diff > noise_threshold)


def filter_intervals(intervals, min_duration):
    """
    Фильтрует интервалы, оставляя только те, длительность которых не меньше min_duration.
    """
    filtered = []
    for interval in intervals:
        if (interval[1] - interval[0]) >= min_duration:
            filtered.append(interval)
    return filtered


def detect_patterns(data, window_size=10, threshold=5.0, min_points=20, noise_threshold=10.0,
                    min_recovery_duration=4, min_drop_duration=6, low_density_threshold=10):
    """
    Обнаруживает интервалы повышения (КВД) и понижения (КПД) давления.

    Параметры:
      data: DataFrame с колонками 'Время (часы)' и 'Давление (атм)'.
      window_size: Размер окна для сглаживания (фильтр Савицкого–Голея).
      threshold: Порог для резкого изменения производной.
      min_points: Минимальное количество точек в интервале.
      noise_threshold: Порог для обнаружения шума в интервале.
      min_recovery_duration: Минимальная длительность интервала повышения (КВД) в часах.
      min_drop_duration: Минимальная длительность интервала понижения (КПД) в часах.
      low_density_threshold: Порог, ниже которого считается, что данные имеют низкую дискретизацию.

    Возвращает:
      recovery_intervals: Список интервалов для КВД в виде [[начало, конец], ...].
      drop_intervals: Список интервалов для КПД в виде [[начало, конец], ...].
    """
    # Извлекаем давление и время
    pressure = data["Давление (атм)"].values
    time = data["Время (часы)"].values

    # Сглаживаем данные
    pressure_smoothed = savgol_filter(pressure, window_size, 3)
    # Вычисляем производную сглаженных данных
    derivative = np.gradient(pressure_smoothed)

    recovery_intervals = []
    drop_intervals = []

    # Обнаружение пиков (интервалы КВД: рост давления)
    peaks = np.where(derivative > threshold)[0]
    for peak in peaks:
        start = max(0, peak - 30)
        end = start + 4 * 60  # 4 часа, если данные с интервалом 10 минут (240 точек)
        if end < len(data):
            if check_point_density(data, start, end, min_points) and not check_for_noise(data, start, end,
                                                                                         noise_threshold):
                recovery_intervals.append([time[start], time[end]])

    # Обнаружение впадин (интервалы КПД: падение давления)
    valleys = np.where(derivative < -threshold)[0]
    for valley in valleys:
        start = max(0, valley - 30)
        end = start + int(1.1 * (valley - start))  # увеличение длительности на 10%
        if end < len(data):
            if check_point_density(data, start, end, min_points) and not check_for_noise(data, start, end,
                                                                                         noise_threshold):
                drop_intervals.append([time[start], time[end]])

    # Фильтрация интервалов по длительности
    recovery_intervals = filter_intervals(recovery_intervals, min_recovery_duration)
    drop_intervals = filter_intervals(drop_intervals, min_drop_duration)

    # Если дискретизация данных низкая, немного расширяем интервалы
    total_duration = time[-1] - time[0]
    if len(data) / total_duration < low_density_threshold:
        recovery_intervals = [[start - 0.1, end + 0.1] for start, end in recovery_intervals]
        drop_intervals = [[start - 0.1, end + 0.1] for start, end in drop_intervals]

    return recovery_intervals, drop_intervals
