import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

# Константы для улучшения читаемости
MIN_POINTS_OFFSET = 30  # ±5 минут при 10-минутном интервале
MIN_RECOVERY_DURATION = 4 * 60  # 4 часа в минутах
MIN_DROP_DURATION = 6 * 60  # 6 часов в минутах
LOW_DENSITY_THRESHOLD = 10  # Порог для низкой дискретности данных


def check_point_density(data, start_idx, end_idx, min_points=20):
    """
    Проверяет плотность точек в интервале.

    Параметры:
        data (pd.DataFrame): Данные с колонками "Время (часы)" и "Давление (атм)".
        start_idx (int): Начальный индекс интервала.
        end_idx (int): Конечный индекс интервала.
        min_points (int): Минимальное количество точек для проверки плотности.

    Возвращает:
        bool: True, если плотность точек достаточна.
    """
    return (end_idx - start_idx) >= min_points


def check_for_noise(data, start_idx, end_idx, noise_threshold=10.0):
    """
    Проверяет наличие шума (резких скачков давления) в интервале.

    Параметры:
        data (pd.DataFrame): Данные с колонками "Время (часы)" и "Давление (атм)".
        start_idx (int): Начальный индекс интервала.
        end_idx (int): Конечный индекс интервала.
        noise_threshold (float): Порог для определения шума.

    Возвращает:
        bool: True, если шум обнаружен.
    """
    pressure_diff = np.abs(np.diff(data["Давление (атм)"][start_idx:end_idx]))
    return np.any(pressure_diff > noise_threshold)


def filter_intervals(intervals, min_duration):
    """
    Фильтрует интервалы по минимальной длительности.

    Параметры:
        intervals (list): Список интервалов в формате [[start1, end1], [start2, end2], ...].
        min_duration (float): Минимальная длительность интервала.

    Возвращает:
        list: Отфильтрованные интервалы.
    """
    return [interval for interval in intervals if (interval[1] - interval[0]) >= min_duration]


def detect_patterns(data, window_size=10, threshold=5.0, min_points=20, noise_threshold=10.0,
                    min_recovery_duration=MIN_RECOVERY_DURATION, min_drop_duration=MIN_DROP_DURATION,
                    low_density_threshold=LOW_DENSITY_THRESHOLD):
    """
    Выделяет интервалы КВД (рост давления) и КПД (падение давления) на основе данных.

    Параметры:
        data (pd.DataFrame): Данные с колонками "Время (часы)" и "Давление (атм)".
        window_size (int): Размер окна для сглаживания.
        threshold (float): Порог для определения резких изменений.
        min_points (int): Минимальное количество точек для проверки плотности.
        noise_threshold (float): Порог для определения шума.
        min_recovery_duration (float): Минимальная длительность интервала КВД.
        min_drop_duration (float): Минимальная длительность интервала КПД.
        low_density_threshold (float): Порог для низкой дискретности данных.

    Возвращает:
        tuple: (recovery_intervals, drop_intervals) - списки интервалов КВД и КПД.
    """
    # Сглаживание данных
    pressure = data["Давление (атм)"].values
    pressure_smoothed = savgol_filter(pressure, window_size, 3)
    derivative = np.gradient(pressure_smoothed)

    recovery_intervals = []
    drop_intervals = []

    # Поиск интервалов КВД (рост давления)
    peaks = np.where(derivative > threshold)[0]
    for peak in peaks:
        start = max(0, peak - MIN_POINTS_OFFSET)
        end = start + MIN_RECOVERY_DURATION
        if (end < len(data)) and check_point_density(data, start, end, min_points) and not check_for_noise(data, start,
                                                                                                           end,
                                                                                                           noise_threshold):
            recovery_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])

    # Поиск интервалов КПД (падение давления)
    valleys = np.where(derivative < -threshold)[0]
    for valley in valleys:
        start = max(0, valley - MIN_POINTS_OFFSET)
        end = start + int(1.1 * (valley - start))
        if (end < len(data)) and check_point_density(data, start, end, min_points) and not check_for_noise(data, start,
                                                                                                           end,
                                                                                                           noise_threshold):
            drop_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])

    # Фильтрация интервалов по длительности
    recovery_intervals = filter_intervals(recovery_intervals, min_recovery_duration)
    drop_intervals = filter_intervals(drop_intervals, min_drop_duration)

    # Учет низкой дискретности данных
    if len(data) / (data["Время (часы)"].max() - data["Время (часы)"].min()) < low_density_threshold:
        recovery_intervals = [[start - 0.1, end + 0.1] for start, end in recovery_intervals]
        drop_intervals = [[start - 0.1, end + 0.1] for start, end in drop_intervals]

    return recovery_intervals, drop_intervals