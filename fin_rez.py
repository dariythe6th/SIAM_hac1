# Финальное тестирование
final_results = []

for file in data_files:
    data = pd.read_csv(os.path.join("data", file))
    data.columns = ["Время (часы)", "Давление (атм)"]
    
    true_intervals = pd.read_csv(os.path.join("true_intervals", file))
    true_recovery = eval(true_intervals["recovery"].iloc[0])
    true_drop = eval(true_intervals["drop"].iloc[0])
    
    recovery_intervals, drop_intervals = detect_patterns(data)
    
    f1_recovery = calculate_f1_score(true_recovery, recovery_intervals)
    f1_drop = calculate_f1_score(true_drop, drop_intervals)
    
    final_results.append({
        "file": file,
        "recovery_intervals": recovery_intervals,
        "drop_intervals": drop_intervals,
        "f1_recovery": f1_recovery,
        "f1_drop": f1_drop
    })

# Вывод финальных результатов
avg_f1_recovery = np.mean([result["f1_recovery"] for result in final_results])
avg_f1_drop = np.mean([result["f1_drop"] for result in final_results])

print("Финальный средний F1-score для КВД:", avg_f1_recovery)
print("Финальный средний F1-score для КПД:", avg_f1_drop)