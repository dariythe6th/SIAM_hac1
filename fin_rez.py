import os
import numpy as np
import pandas as pd
from f1score import calculate_f1_score
from search import detect_patterns
from utils import safe_parse_intervals

final_results = []
data_files = [f for f in os.listdir("data") if f.endswith(".csv")]

for file in data_files:
    data = pd.read_csv(os.path.join("data", file))
    data.columns = ["Время (часы)", "Давление (атм)"]

    true_intervals = pd.read_csv(os.path.join("true_intervals", file))
    true_recovery = safe_parse_intervals(true_intervals["recovery"].iloc[0])
    true_drop = safe_parse_intervals(true_intervals["drop"].iloc[0])

    recovery_intervals, drop_intervals = detect_patterns(data)

    f1_recovery = calculate_f1_score(true_recovery, recovery_intervals, data)
    f1_drop = calculate_f1_score(true_drop, drop_intervals, data)

    final_results.append({
        "file": file,
        "recovery_intervals": recovery_intervals,
        "drop_intervals": drop_intervals,
        "f1_recovery": f1_recovery,
        "f1_drop": f1_drop
    })

avg_f1_recovery = np.mean([r["f1_recovery"] for r in final_results])
avg_f1_drop = np.mean([r["f1_drop"] for r in final_results])

print("Финальный средний F1-score для КВД:", avg_f1_recovery)
print("Финальный средний F1-score для КПД:", avg_f1_drop)
