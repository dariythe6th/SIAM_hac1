# Формирование финального CSV-файла
final_submission = []

for result in final_results:
    final_submission.append({
        "file": result["file"],
        "recovery": result["recovery_intervals"],
        "drop": result["drop_intervals"]
    })

final_submission_df = pd.DataFrame(final_submission)
final_submission_df.to_csv("final_submission.csv", index=False)