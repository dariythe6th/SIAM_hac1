import pandas as pd
from search import detect_patterns
from visual import plot_intervals
from f1score import calculate_f1_score
from utils import safe_parse_intervals

# Пример использования синтетических данных
synthetic_data = [
    (0, 300),
    (5, 235.622483502636),
    (10, 207.896596280238),
    # ... (дополнить данными из Приложения 3)
    (1300, 110.851256713742)
]
synthetic_df = pd.DataFrame(synthetic_data, columns=["Время (часы)", "Давление (атм)"])

recovery_intervals, drop_intervals = detect_patterns(synthetic_df)
print("КВД интервалы:", recovery_intervals)
print("КПД интервалы:", drop_intervals)

# Загрузка реальных данных
real_data = pd.read_csv("real_well_data.csv")
real_data.columns = ["Время (часы)", "Давление (атм)"]

true_intervals = pd.read_csv("true_intervals.csv")
true_recovery = safe_parse_intervals(true_intervals["recovery"].iloc[0])
true_drop = safe_parse_intervals(true_intervals["drop"].iloc[0])

recovery_intervals, drop_intervals = detect_patterns(real_data)
print("КВД интервалы:", recovery_intervals)
print("КПД интервалы:", drop_intervals)

# Визуализация результатов
plot_intervals(real_data, recovery_intervals, drop_intervals)

# Оценка качества на реальных данных
f1_recovery = calculate_f1_score(true_recovery, recovery_intervals, real_data)
f1_drop = calculate_f1_score(true_drop, drop_intervals, real_data)

print("F1-score для КВД на реальных данных:", f1_recovery)
print("F1-score для КПД на реальных данных:", f1_drop)
