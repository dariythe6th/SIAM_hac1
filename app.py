import os
import pandas as pd
from search import detect_patterns
from visual import plot_intervals  # Импортируем функцию для визуализации

# Загрузка всех данных из папки data
data_files = [f for f in os.listdir("data") if f.endswith(".csv")]
all_results = []

for file in data_files:
    # Загрузка данных
    data = pd.read_csv(os.path.join("data", file))
    data.columns = ["Время (часы)", "Давление (атм)"]

    # Применение алгоритма для выделения интервалов
    recovery_intervals, drop_intervals = detect_patterns(data)

    # Сохранение результатов
    all_results.append({
        "file": file,
        "recovery_intervals": recovery_intervals,
        "drop_intervals": drop_intervals
    })

    # Визуализация результатов для каждого файла
    plot_intervals(data, recovery_intervals, drop_intervals)

# Вывод результатов
for result in all_results:
    print(f"Файл: {result['file']}")
    print("Интервалы КВД:", result["recovery_intervals"])
    print("Интервалы КПД:", result["drop_intervals"])
    print("-" * 40)