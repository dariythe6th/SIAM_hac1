from sklearn.metrics import f1_score

def calculate_f1_score(true_intervals, pred_intervals, time_tolerance=0.08333):
    # Преобразуем интервалы в бинарные метки
    true_labels = np.zeros(len(data))
    pred_labels = np.zeros(len(data))
    
    for interval in true_intervals:
        start_idx = np.searchsorted(data["Время (часы)"], interval[0] - time_tolerance)
        end_idx = np.searchsorted(data["Время (часы)"], interval[1] + time_tolerance)
        true_labels[start_idx:end_idx] = 1
    
    for interval in pred_intervals:
        start_idx = np.searchsorted(data["Время (часы)"], interval[0] - time_tolerance)
        end_idx = np.searchsorted(data["Время (часы)"], interval[1] + time_tolerance)
        pred_labels[start_idx:end_idx] = 1
    
    return f1_score(true_labels, pred_labels)

# Пример использования
true_recovery = [[100, 300]]  # Пример эталонных интервалов
true_drop = [[500, 700]]
f1_recovery = calculate_f1_score(true_recovery, recovery_intervals)
f1_drop = calculate_f1_score(true_drop, drop_intervals)

print("F1-score для КВД:", f1_recovery)
print("F1-score для КПД:", f1_drop)