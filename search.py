import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
import config

def check_point_density(data: pd.DataFrame, start_idx: int, end_idx: int, min_points: int = config.MIN_POINTS) -> bool:
    """
    Проверяет, что в интервале имеется достаточное количество точек.
    Считает точки в первые 1 час (например, 6 точек при 10-минутном интервале).
    """
    first_hour_end = start_idx + 6
    if first_hour_end > end_idx:
        return False
    return (end_idx - start_idx) >= min_points

def check_for_noise(data: pd.DataFrame, start_idx: int, end_idx: int, noise_threshold: float = config.NOISE_THRESHOLD) -> bool:
    """
    Проверяет наличие резких скачков давления в интервале.
    Если разница между соседними точками превышает noise_threshold, интервал считается зашумленным.
    """
    pressure_diff = np.abs(np.diff(data["Давление (атм)"][start_idx:end_idx]))
    return np.any(pressure_diff > noise_threshold)

def filter_intervals(intervals: list, min_duration: float) -> list:
    """
    Фильтрует интервалы, оставляя только те, длительность которых не меньше min_duration.
    """
    filtered = []
    for interval in intervals:
        if (interval[1] - interval[0]) >= min_duration:
            filtered.append(interval)
    return filtered

def detect_patterns(data: pd.DataFrame,
                    window_size: int = config.WINDOW_SIZE,
                    threshold: float = config.THRESHOLD,
                    min_points: int = config.MIN_POINTS,
                    noise_threshold: float = config.NOISE_THRESHOLD,
                    min_recovery_duration: float = config.MIN_RECOVERY_DURATION,
                    min_drop_duration: float = config.MIN_DROP_DURATION,
                    low_density_threshold: float = config.LOW_DENSITY_THRESHOLD) -> tuple:
    """
    Обнаруживает интервалы повышения (КВД) и понижения (КПД) давления.

    Аргументы:
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
    pressure = data["Давление (атм)"].values
    time = data["Время (часы)"].values

    # Проверка: window_size должен быть нечетным и меньше размера данных
    if window_size % 2 == 0:
        raise ValueError("Размер окна должен быть нечетным для фильтра Савицкого–Голея.")
    if window_size > len(data):
        raise ValueError("Размер окна больше, чем количество точек данных.")

    # Сглаживание данных
    pressure_smoothed = savgol_filter(pressure, window_size, config.POLYORDER)
    derivative = np.gradient(pressure_smoothed)

    recovery_intervals = []
    drop_intervals = []

    # Обнаружение пиков (интервалы КВД: рост давления)
    peaks = np.where(derivative > threshold)[0]
    for peak in peaks:
        start = max(0, peak - config.PEAK_OFFSET)
        end = start + config.RECOVERY_DURATION_POINTS
        if end < len(data):
            if check_point_density(data, start, end, min_points) and not check_for_noise(data, start, end, noise_threshold):
                recovery_intervals.append([time[start], time[end]])

    # Обнаружение впадин (интервалы КПД: падение давления)
    valleys = np.where(derivative < -threshold)[0]
    for valley in valleys:
        start = max(0, valley - config.PEAK_OFFSET)
        # Рассчитываем длительность интервала с увеличением на 10%
        end = start + int(1.1 * (valley - start))
        if end < len(data):
            if check_point_density(data, start, end, min_points) and not check_for_noise(data, start, end, noise_threshold):
                drop_intervals.append([time[start], time[end]])

    recovery_intervals = filter_intervals(recovery_intervals, min_recovery_duration)
    drop_intervals = filter_intervals(drop_intervals, min_drop_duration)

    # При низкой дискретизации расширяем интервалы
    total_duration = time[-1] - time[0]
    if len(data) / total_duration < low_density_threshold:
        recovery_intervals = [[start - 0.1, end + 0.1] for start, end in recovery_intervals]
        drop_intervals = [[start - 0.1, end + 0.1] for start, end in drop_intervals]

    return recovery_intervals, drop_intervals

