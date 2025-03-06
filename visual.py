import matplotlib.pyplot as plt


def plot_intervals(data, recovery_intervals, drop_intervals):
    """
    Визуализирует данные с выделенными интервалами КВД и КПД.

    Параметры:
        data (pd.DataFrame): Данные с колонками "Время (часы)" и "Давление (атм)".
        recovery_intervals (list): Интервалы КВД.
        drop_intervals (list): Интервалы КПД.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data["Время (часы)"], data["Давление (атм)"], label="Давление")

    for interval in recovery_intervals:
        plt.axvspan(interval[0], interval[1], color='green', alpha=0.3,
                    label="КВД" if not recovery_intervals.index(interval) else "")

    for interval in drop_intervals:
        plt.axvspan(interval[0], interval[1], color='red', alpha=0.3,
                    label="КПД" if not drop_intervals.index(interval) else "")

    plt.xlabel("Время (часы)")
    plt.ylabel("Давление (атм)")
    plt.title("Выделение интервалов КВД и КПД")
    plt.legend()
    plt.grid()
    plt.show()


# Пример использования
if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    from search import detect_patterns

    # Создаем синтетические данные
    synthetic_data = pd.DataFrame({
        "Время (часы)": np.arange(0, 1000, 10),
        "Давление (атм)": np.sin(np.arange(0, 1000, 10) * 0.1) * 100
    })

    # Применяем алгоритм
    recovery_intervals, drop_intervals = detect_patterns(synthetic_data)

    # Визуализация
    plot_intervals(synthetic_data, recovery_intervals, drop_intervals)