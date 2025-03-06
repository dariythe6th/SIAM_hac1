import json
import os
import numpy as np
import pandas as pd
from search import detect_patterns
from f1score import calculate_f1_score

def load_data_and_true_intervals(file):
    """
    Загружает данные и эталонные интервалы для одного файла.

    Параметры:
        file (str): Имя файла с данными.

    Возвращает:
        tuple: (data, true_recovery, true_drop) - данные и эталонные интервалы.
    """
    # Загрузка данных
    data = pd.read_csv(os.path.join("data", file))
    data.columns = ["Время (часы)", "Давление (атм)"]

    # Загрузка эталонной разметки
    true_intervals = pd.read_csv(os.path.join("true_intervals", file))
    true_recovery = json.loads(true_intervals["recovery"].iloc[0].replace(" ", ","))
    true_drop = json.loads(true_intervals["drop"].iloc[0].replace(" ", ","))

    return data, true_recovery, true_drop

def analyze_file(file):
    """
    Анализирует один файл: применяет алгоритм и вычисляет F1-score.

    Параметры:
        file (str): Имя файла с данными.

    Возвращает:
        dict: Результаты анализа.
    """
    data, true_recovery, true_drop = load_data_and_true_intervals(file)

    # Применение алгоритма
    recovery_intervals, drop_intervals = detect_patterns(data)

    # Оценка качества
    f1_recovery = calculate_f1_score(true_recovery, recovery_intervals, data)
    f1_drop = calculate_f1_score(true_drop, drop_intervals, data)

    return {
        "file": file,
        "recovery_intervals": recovery_intervals,
        "drop_intervals": drop_intervals,
        "f1_recovery": f1_recovery,
        "f1_drop": f1_drop
    }

def analyze_all_files():
    """
    Анализирует все файлы в папке data и возвращает результаты.

    Возвращает:
        list: Список результатов анализа.
    """
    data_files = [f for f in os.listdir("data") if f.endswith(".csv")]
    all_results = [analyze_file(file) for file in data_files]
    return all_results

def calculate_average_f1_scores(all_results):
    """
    Вычисляет средние значения F1-score для всех результатов.

    Параметры:
        all_results (list): Список результатов анализа.

    Возвращает:
        tuple: (avg_f1_recovery, avg_f1_drop) - средние значения F1-score.
    """
    avg_f1_recovery = np.mean([result["f1_recovery"] for result in all_results])
    avg_f1_drop = np.mean([result["f1_drop"] for result in all_results])
    return avg_f1_recovery, avg_f1_drop

def get_worst_results(all_results, n=5):
    """
    Возвращает n худших результатов по среднему F1-score.

    Параметры:
        all_results (list): Список результатов анализа.
        n (int): Количество худших результатов для возврата.

    Возвращает:
        list: Список худших результатов.
    """
    return sorted(all_results, key=lambda x: (x["f1_recovery"] + x["f1_drop"]) / 2)[:n]