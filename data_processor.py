import os
import pandas as pd
from utils import safe_parse_intervals
from search import detect_patterns
from f1score import calculate_f1_score

class DataProcessor:
    """
    Класс для обработки данных, загрузки истинной разметки и оценки качества алгоритма.
    """
    def __init__(self, data_dir, intervals_dir):
        """
        Инициализация с указанием директорий с данными и истинной разметкой.
        """
        self.data_dir = data_dir
        self.intervals_dir = intervals_dir

    def load_data(self, filename):
        """
        Загружает данные из CSV-файла и переименовывает колонки.
        """
        data = pd.read_csv(os.path.join(self.data_dir, filename))
        data.columns = ["Время (часы)", "Давление (атм)"]
        return data

    def load_intervals(self, filename):
        """
        Загружает истинные интервалы из CSV-файла с использованием безопасного парсера.
        """
        true_intervals = pd.read_csv(os.path.join(self.intervals_dir, filename))
        true_recovery = safe_parse_intervals(true_intervals["recovery"].iloc[0])
        true_drop = safe_parse_intervals(true_intervals["drop"].iloc[0])
        return true_recovery, true_drop

    def process_file(self, filename, detect_params={}):
        """
        Обрабатывает один файл: загружает данные и истинные интервалы, применяет алгоритм,
        вычисляет F1-score и возвращает результаты в виде словаря.
        """
        data = self.load_data(filename)
        true_recovery, true_drop = self.load_intervals(filename)
        recovery_intervals, drop_intervals = detect_patterns(data, **detect_params)
        f1_recovery = calculate_f1_score(true_recovery, recovery_intervals, data)
        f1_drop = calculate_f1_score(true_drop, drop_intervals, data)
        return {
            "file": filename,
            "data": data,
            "recovery_intervals": recovery_intervals,
            "drop_intervals": drop_intervals,
            "f1_recovery": f1_recovery,
            "f1_drop": f1_drop
        }
