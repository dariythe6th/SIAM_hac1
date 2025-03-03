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