import matplotlib.pyplot as plt

def plot_intervals(data, recovery_intervals, drop_intervals):
    plt.figure(figsize=(12, 6))
    plt.plot(data["Время (часы)"], data["Давление (атм)"], label="Давление")
    
    for interval in recovery_intervals:
        plt.axvspan(interval[0], interval[1], color='green', alpha=0.3, label="КВД" if not recovery_intervals.index(interval) else "")
    
    for interval in drop_intervals:
        plt.axvspan(interval[0], interval[1], color='red', alpha=0.3, label="КПД" if not drop_intervals.index(interval) else "")
    
    plt.xlabel("Время (часы)")
    plt.ylabel("Давление (атм)")
    plt.title("Выделение интервалов КВД и КПД")
    plt.legend()
    plt.grid()
    plt.show()

# Визуализация результатов
plot_intervals(synthetic_df, recovery_intervals, drop_intervals)