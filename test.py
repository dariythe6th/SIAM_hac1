# Пример использования синтетических данных
synthetic_data = [
    (0, 300),
    (5, 235.622483502636),
    (10, 207.896596280238),
    # ... (дополнить данными из Приложения 3)
    (1300, 110.851256713742)
]

# Преобразуем данные в DataFrame
synthetic_df = pd.DataFrame(synthetic_data, columns=["Время (часы)", "Давление (атм)"])

# Применяем алгоритм
recovery_intervals, drop_intervals = detect_patterns(synthetic_df)

# Вывод результатов
print("КВД интервалы:", recovery_intervals)
print("КПД интервалы:", drop_intervals)

# Загрузка реальных данных
real_data = pd.read_csv("real_well_data.csv")
real_data.columns = ["Время (часы)", "Давление (атм)"]

# Загрузка эталонной разметки
true_intervals = pd.read_csv("true_intervals.csv")
true_recovery = eval(true_intervals["recovery"].iloc[0])  # Пример: [[1420.98, 2438.42], [2178.79, 3454.68]]
true_drop = eval(true_intervals["drop"].iloc[0])          # Пример: [[4454.68, 4764.96]]
# Применение алгоритма к реальным данным
recovery_intervals, drop_intervals = detect_patterns(real_data)

# Вывод результатов
print("КВД интервалы:", recovery_intervals)
print("КПД интервалы:", drop_intervals)
# Визуализация результатов для реальных данных
plot_intervals(real_data, recovery_intervals, drop_intervals)

# Оценка качества на реальных данных
f1_recovery = calculate_f1_score(true_recovery, recovery_intervals)
f1_drop = calculate_f1_score(true_drop, drop_intervals)

print("F1-score для КВД на реальных данных:", f1_recovery)
print("F1-score для КПД на реальных данных:", f1_drop)