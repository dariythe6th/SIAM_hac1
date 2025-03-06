from core import analyze_all_files, calculate_average_f1_scores

# Финальное тестирование
final_results = analyze_all_files()

# Вывод финальных результатов
avg_f1_recovery, avg_f1_drop = calculate_average_f1_scores(final_results)
print("Финальный средний F1-score для КВД:", avg_f1_recovery)
print("Финальный средний F1-score для КПД:", avg_f1_drop)