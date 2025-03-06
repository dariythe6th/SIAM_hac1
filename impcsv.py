import pandas as pd
from core import analyze_all_files

# Анализ всех файлов и получение результатов
final_results = analyze_all_files()

# Формирование финального CSV-файла
final_submission = []

for result in final_results:
    final_submission.append({
        "file": result["file"],
        "recovery": result["recovery_intervals"],
        "drop": result["drop_intervals"]
    })

# Создание DataFrame и сохранение в CSV
final_submission_df = pd.DataFrame(final_submission)
final_submission_df.to_csv("final_submission.csv", index=False)

print("Финальный CSV-файл успешно создан: final_submission.csv")