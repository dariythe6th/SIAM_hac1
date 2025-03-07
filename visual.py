import matplotlib.pyplot as plt


def plot_intervals(data, recovery_intervals, drop_intervals):
    """
    Визуализация временных рядов давления с выделенными интервалами КВД и КПД.

    Аргументы:
      data: DataFrame с колонками "Время (часы)" и "Давление (атм)".
      recovery_intervals: Список интервалов для КВД, например, [[начало, конец], ...].
      drop_intervals: Список интервалов для КПД.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data["Время (часы)"], data["Давление (атм)"], label="Давление")

    # Отображение интервалов КВД
    for idx, interval in enumerate(recovery_intervals):
        plt.axvspan(interval[0], interval[1], color='green', alpha=0.3,
                    label="КВД" if idx == 0 else "")

    # Отображение интервалов КПД
    for idx, interval in enumerate(drop_intervals):
        plt.axvspan(interval[0], interval[1], color='red', alpha=0.3,
                    label="КПД" if idx == 0 else "")

    plt.xlabel("Время (часы)")
    plt.ylabel("Давление (атм)")
    plt.title("Выделение интервалов КВД и КПД")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    import pandas as pd

    # Пример данных
    synthetic_data = [
        (0, 300),
        (5, 235.622483502636),
        (10, 207.896596280238),
        # ... (дополнить данными)
        (1300, 110.851256713742)
    ]
    synthetic_df = pd.DataFrame(synthetic_data, columns=["Время (часы)", "Давление (атм)"])

    recovery_intervals = [[100, 300]]  # Пример интервалов КВД
    drop_intervals = [[500, 700]]  # Пример интервалов КПД

    plot_intervals(synthetic_df, recovery_intervals, drop_intervals)
