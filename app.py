from core import analyze_all_files, calculate_average_f1_scores, get_worst_results

# Анализ всех файлов
all_results = analyze_all_files()

# Вывод среднего F1-score
avg_f1_recovery, avg_f1_drop = calculate_average_f1_scores(all_results)
print("Средний F1-score для КВД:", avg_f1_recovery)
print("Средний F1-score для КПД:", avg_f1_drop)

# Анализ худших результатов
worst_results = get_worst_results(all_results)
for result in worst_results:
    print(f"Файл: {result['file']}, F1 КВД: {result['f1_recovery']}, F1 КПД: {result['f1_drop']}")