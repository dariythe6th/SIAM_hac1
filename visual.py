import matplotlib.pyplot as plt

def plot_intervals(data, recovery_intervals, drop_intervals):
    """
    Визуализация временных рядов давления с выделенными интервалами КВД и КПД.

    Параметры:
    - data: DataFrame с колонками "Время (часы)" и "Давление (атм)".
    - recovery_intervals: Список интервалов КВД (например, [[start1, end1], [start2, end2]]).
    - drop_intervals: Список интервалов КПД (например, [[start1, end1], [start2, end2]]).
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data["Время (часы)"], data["Давление (атм)"], label="Давление")

    # Визуализация интервалов КВД
    for interval in recovery_intervals:
        plt.axvspan(interval[0], interval[1], color='green', alpha=0.3,
                    label="КВД" if not recovery_intervals.index(interval) else "")

    # Визуализация интервалов КПД
    for interval in drop_intervals:
        plt.axvspan(interval[0], interval[1], color='red', alpha=0.3,
                    label="КПД" if not drop_intervals.index(interval) else "")

    plt.xlabel("Время (часы)")
    plt.ylabel("Давление (атм)")
    plt.title("Выделение интервалов КВД и КПД")
    plt.legend()
    plt.grid()
    plt.show()


# Пример использования (выполняется только при запуске файла напрямую)
if __name__ == "__main__":
    import pandas as pd

    # Пример данных
    synthetic_data = [
        (0, 300),
        (5, 235.622483502636),
        (10, 207.896596280238),
        # ... (дополнить данными из Приложения 3)
        (1300, 110.851256713742)
    ]

    # Преобразуем данные в DataFrame
    synthetic_df = pd.DataFrame(synthetic_data, columns=["Время (часы)", "Давление (атм)"])

    # Пример интервалов
    recovery_intervals = [[100, 300]]  # Пример интервалов КВД
    drop_intervals = [[500, 700]]  # Пример интервалов КПД

    # Визуализация результатов
    plot_intervals(synthetic_df, recovery_intervals, drop_intervals)