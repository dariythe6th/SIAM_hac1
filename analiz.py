import os
import numpy as np
import pandas as pd
from f1score import calculate_f1_score
from search import detect_patterns
from utils import safe_parse_intervals

# Загрузка всех файлов из папки data
data_files = [f for f in os.listdir("data") if f.endswith(".csv")]
all_results = []

for file in data_files:
    # Загрузка данных
    data = pd.read_csv(os.path.join("data", file))
    data.columns = ["Время (часы)", "Давление (атм)"]

    # Загрузка эталонной разметки с использованием безопасного парсера
    true_intervals = pd.read_csv(os.path.join("true_intervals", file))
    true_recovery = safe_parse_intervals(true_intervals["recovery"].iloc[0])
    true_drop = safe_parse_intervals(true_intervals["drop"].iloc[0])

    # Применение алгоритма
    recovery_intervals, drop_intervals = detect_patterns(data)

    # Оценка качества с передачей исходных данных
    f1_recovery = calculate_f1_score(true_recovery, recovery_intervals, data)
    f1_drop = calculate_f1_score(true_drop, drop_intervals, data)

    all_results.append({
        "file": file,
        "recovery_intervals": recovery_intervals,
        "drop_intervals": drop_intervals,
        "f1_recovery": f1_recovery,
        "f1_drop": f1_drop
    })

# Вычисление и вывод среднего F1-score
avg_f1_recovery = np.mean([r["f1_recovery"] for r in all_results])
avg_f1_drop = np.mean([r["f1_drop"] for r in all_results])

print("Средний F1-score для КВД:", avg_f1_recovery)
print("Средний F1-score для КПД:", avg_f1_drop)

# Анализ 5 худших результатов
worst_results = sorted(all_results, key=lambda x: (x["f1_recovery"] + x["f1_drop"]) / 2)[:5]
for result in worst_results:
    print(f"Файл: {result['file']}, F1 КВД: {result['f1_recovery']}, F1 КПД: {result['f1_drop']}")
