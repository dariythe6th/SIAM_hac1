import os
import numpy as np
import pandas as pd
import logging
from f1score import calculate_f1_score
from search import detect_patterns
from utils import safe_parse_intervals

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def process_files(data_dir: str = "data", intervals_dir: str = "true_intervals") -> None:
    """
    Обрабатывает все CSV-файлы в указанной папке data, сравнивает найденные интервалы с истинной разметкой
    и вычисляет F1-score для каждого файла.
    """
    data_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    all_results = []

    for file in data_files:
        try:
            data_path = os.path.join(data_dir, file)
            data = pd.read_csv(data_path)
            data.columns = ["Время (часы)", "Давление (атм)"]
        except Exception as e:
            logging.error(f"Ошибка при загрузке файла {file}: {e}")
            continue

        try:
            true_intervals = pd.read_csv(os.path.join(intervals_dir, file))
            true_recovery = safe_parse_intervals(true_intervals["recovery"].iloc[0])
            true_drop = safe_parse_intervals(true_intervals["drop"].iloc[0])
        except Exception as e:
            logging.error(f"Ошибка при загрузке истинных интервалов для файла {file}: {e}")
            continue

        try:
            recovery_intervals, drop_intervals = detect_patterns(data)
            f1_recovery = calculate_f1_score(true_recovery, recovery_intervals, data)
            f1_drop = calculate_f1_score(true_drop, drop_intervals, data)
        except Exception as e:
            logging.error(f"Ошибка при обработке файла {file}: {e}")
            continue

        all_results.append({
            "file": file,
            "recovery_intervals": recovery_intervals,
            "drop_intervals": drop_intervals,
            "f1_recovery": f1_recovery,
            "f1_drop": f1_drop
        })

    if all_results:
        avg_f1_recovery = np.mean([r["f1_recovery"] for r in all_results])
        avg_f1_drop = np.mean([r["f1_drop"] for r in all_results])
        logging.info(f"Средний F1-score для КВД: {avg_f1_recovery}")
        logging.info(f"Средний F1-score для КПД: {avg_f1_drop}")

        worst_results = sorted(all_results, key=lambda x: (x["f1_recovery"] + x["f1_drop"]) / 2)[:5]
        for result in worst_results:
            logging.info(f"Файл: {result['file']}, F1 КВД: {result['f1_recovery']}, F1 КПД: {result['f1_drop']}")
    else:
        logging.warning("Нет результатов для обработки.")


if __name__ == "__main__":
    process_files()

