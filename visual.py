import pandas as pd
import matplotlib.pyplot as plt
from search import detect_patterns  # Импортируем функцию для обнаружения интервалов

def plot_intervals(data, recovery_intervals, drop_intervals):
    """
    Визуализация временных рядов давления с выделенными интервалами КВД и КПД.

    Аргументы:
      data: DataFrame с колонками "Время (часы)" и "Давление (атм)".
      recovery_intervals: Список интервалов для КВД, например, [[начало, конец], ...].
      drop_intervals: Список интервалов для КПД.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data["Время (часы)"], data["Давление (атм)"], label="Давление", color='blue')

    # Отображение интервалов КВД
    for idx, interval in enumerate(recovery_intervals):
        plt.axvspan(interval[0], interval[1], color='green', alpha=0.3, label="КВД" if idx == 0 else "")

    # Отображение интервалов КПД
    for idx, interval in enumerate(drop_intervals):
        plt.axvspan(interval[0], interval[1], color='red', alpha=0.3, label="КПД" if idx == 0 else "")

    # Настройка графика
    plt.xlabel("Время (часы)")
    plt.ylabel("Давление (атм)")
    plt.title("Выделение интервалов КВД и КПД")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # Загрузка данных из well_data.csv
    data = pd.read_csv("well_data.csv")
    data.columns = ["Время (часы)", "Давление (атм)"]

    # Применение алгоритма для обнаружения интервалов
    recovery_intervals, drop_intervals = detect_patterns(data)

    # Визуализация результатов
    plot_intervals(data, recovery_intervals, drop_intervals)