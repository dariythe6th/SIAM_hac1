import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

def check_point_density(data, start_idx, end_idx, min_points=20):
    # Проверка плотности точек в первые 1 час
    first_hour_end = start_idx + 6  # 6 точек при 10-минутном интервале (1 час)
    if first_hour_end > end_idx:
        return False
    return (end_idx - start_idx) >= min_points

# Обновление функции detect_patterns
def detect_patterns(data, window_size=10, threshold=5.0, min_points=20):
    pressure = data["Давление (атм)"].values
    pressure_smoothed = savgol_filter(pressure, window_size, 3)
    derivative = np.gradient(pressure_smoothed)
    
    recovery_intervals = []
    drop_intervals = []
    
    peaks = np.where(derivative > threshold)[0]
    for peak in peaks:
        start = max(0, peak - 30)
        end = start + 4 * 60
        if end < len(data) and check_point_density(data, start, end, min_points):
            recovery_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])
    
    valleys = np.where(derivative < -threshold)[0]
    for valley in valleys:
        start = max(0, valley - 30)
        end = start + int(1.1 * (valley - start))
        if end < len(data) and check_point_density(data, start, end, min_points):
            drop_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])
    
    return recovery_intervals, drop_intervals

def check_for_noise(data, start_idx, end_idx, noise_threshold=10.0):
    # Проверка на резкие скачки давления внутри интервала
    pressure_diff = np.abs(np.diff(data["Давление (атм)"][start_idx:end_idx]))
    return np.any(pressure_diff > noise_threshold)

# Обновление функции detect_patterns
def detect_patterns(data, window_size=10, threshold=5.0, min_points=20, noise_threshold=10.0):
    pressure = data["Давление (атм)"].values
    pressure_smoothed = savgol_filter(pressure, window_size, 3)
    derivative = np.gradient(pressure_smoothed)
    
    recovery_intervals = []
    drop_intervals = []
    
    peaks = np.where(derivative > threshold)[0]
    for peak in peaks:
        start = max(0, peak - 30)
        end = start + 4 * 60
        if end < len(data) and check_point_density(data, start, end, min_points) and not check_for_noise(data, start, end, noise_threshold):
            recovery_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])
    
    valleys = np.where(derivative < -threshold)[0]
    for valley in valleys:
        start = max(0, valley - 30)
        end = start + int(1.1 * (valley - start))
        if end < len(data) and check_point_density(data, start, end, min_points) and not check_for_noise(data, start, end, noise_threshold):
            drop_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])
    
    return recovery_intervals, drop_intervals

def detect_patterns(data, window_size=10, threshold=5.0):
    # Сглаживание данных
    pressure = data["Давление (атм)"].values
    pressure_smoothed = savgol_filter(pressure, window_size, 3)
    
    # Расчет производной
    derivative = np.gradient(pressure_smoothed)
    
    # Поиск резких изменений
    recovery_intervals = []
    drop_intervals = []
    
    # Для КВД (рост давления)
    peaks = np.where(derivative > threshold)[0]
    for peak in peaks:
        start = max(0, peak - 30)  # ±5 минут (30 точек при 10-минутном интервале)
        end = start + 4 * 60       # Минимум 4 часа (240 точек)
        if end < len(data):
            recovery_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])
    
    # Для КПД (падение давления)
    valleys = np.where(derivative < -threshold)[0]
    for valley in valleys:
        start = max(0, valley - 30)
        end = start + int(1.1 * (valley - start))  # +10% длительности
        if end < len(data):
            drop_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])
    
    return recovery_intervals, drop_intervals

def detect_patterns(data, window_size=10, threshold=5.0, min_points=20, noise_threshold=10.0, min_recovery_duration=4, min_drop_duration=6, low_density_threshold=10):
    pressure = data["Время (часы)"].values
    pressure_smoothed = savgol_filter(pressure, window_size, 3)
    derivative = np.gradient(pressure_smoothed)
    
    recovery_intervals = []
    drop_intervals = []
    
    peaks = np.where(derivative > threshold)[0]
    for peak in peaks:
        start = max(0, peak - 30)
        end = start + 4 * 60
        if end < len(data) and check_point_density(data, start, end, min_points) and not check_for_noise(data, start, end, noise_threshold):
            recovery_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])
    
    valleys = np.where(derivative < -threshold)[0]
    for valley in valleys:
        start = max(0, valley - 30)
        end = start + int(1.1 * (valley - start))
        if end < len(data) and check_point_density(data, start, end, min_points) and not check_for_noise(data, start, end, noise_threshold):
            drop_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])
    
    # Фильтрация интервалов по длительности
    recovery_intervals = filter_intervals(recovery_intervals, min_recovery_duration)
    drop_intervals = filter_intervals(drop_intervals, min_drop_duration)
    
    # Учет низкой дискретности
    if len(data) / (data["Время (часы)"].max() - data["Время (часы)"].min()) < low_density_threshold:
        # Увеличиваем допустимые отклонения
        recovery_intervals = [[start - 0.1, end + 0.1] for start, end in recovery_intervals]
        drop_intervals = [[start - 0.1, end + 0.1] for start, end in drop_intervals]
    
    return recovery_intervals, drop_intervals


def filter_intervals(intervals, min_duration):
    # Фильтрация интервалов по минимальной длительности
    filtered = []
    for interval in intervals:
        duration = interval[1] - interval[0]
        if duration >= min_duration:
            filtered.append(interval)
    return filtered

# Обновление функции detect_patterns
def detect_patterns(data, window_size=10, threshold=5.0, min_points=20, noise_threshold=10.0, min_recovery_duration=4, min_drop_duration=6):
    pressure = data["Давление (атм)"].values
    pressure_smoothed = savgol_filter(pressure, window_size, 3)
    derivative = np.gradient(pressure_smoothed)
    
    recovery_intervals = []
    drop_intervals = []
    
    peaks = np.where(derivative > threshold)[0]
    for peak in peaks:
        start = max(0, peak - 30)
        end = start + 4 * 60
        if end < len(data) and check_point_density(data, start, end, min_points) and not check_for_noise(data, start, end, noise_threshold):
            recovery_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])
    
    valleys = np.where(derivative < -threshold)[0]
    for valley in valleys:
        start = max(0, valley - 30)
        end = start + int(1.1 * (valley - start))
        if end < len(data) and check_point_density(data, start, end, min_points) and not check_for_noise(data, start, end, noise_threshold):
            drop_intervals.append([data["Время (часы)"][start], data["Время (часы)"][end]])
    
    # Фильтрация интервалов по длительности
    recovery_intervals = filter_intervals(recovery_intervals, min_recovery_duration)
    drop_intervals = filter_intervals(drop_intervals, min_drop_duration)
    
    return recovery_intervals, drop_intervals

# Загрузка данных
data = pd.read_csv("data/well_data.csv")
recovery, drop = detect_patterns(data)

# Сохранение в CSV
result = pd.DataFrame({
    "file": ["data/well_data.csv"],
    "recovery": [recovery],
    "drop": [drop]
})
result.to_csv("submission.csv", index=False)