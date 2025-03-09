import numpy as np
import pandas as pd
from sklearn.metrics import f1_score


def calculate_mae(true_intervals, pred_intervals):
    """
    Вычисляет среднюю абсолютную ошибку (MAE) для интервалов.
    """
    mae = 0
    count = 0

    for true, pred in zip(true_intervals, pred_intervals):
        start_error = abs(true[0] - pred[0])
        end_error = abs(true[1] - pred[1])

        mae += (start_error + end_error) / 2
        count += 1

    return mae / count if count > 0 else 0


def calculate_f1_score(true_intervals, pred_intervals, data, time_tolerance=0.08333, mae_threshold=0.15):
    """
    Вычисляет F1-score для обнаружения интервалов, переводя интервалы в бинарные метки,
    с фильтрацией true positive на основе MAE.
    """
    true_labels = np.zeros(len(data))
    pred_labels = np.zeros(len(data))

    # Фильтруем интервалы с MAE > mae_threshold
    filtered_true_intervals = []
    filtered_pred_intervals = []

    for true, pred in zip(true_intervals, pred_intervals):
        mae = calculate_mae([true], [pred])

        if mae <= mae_threshold:
            filtered_true_intervals.append(true)
            filtered_pred_intervals.append(pred)

    # Создаем бинарные метки для истинных интервалов
    for interval in filtered_true_intervals:
        start_idx = np.searchsorted(data["Время (часы)"], interval[0] - time_tolerance)
        end_idx = np.searchsorted(data["Время (часы)"], interval[1] + time_tolerance)
        true_labels[start_idx:end_idx] = 1

    # Создаем бинарные метки для предсказанных интервалов
    for interval in filtered_pred_intervals:
        start_idx = np.searchsorted(data["Время (часы)"], interval[0] - time_tolerance)
        end_idx = np.searchsorted(data["Время (часы)"], interval[1] + time_tolerance)
        pred_labels[start_idx:end_idx] = 1

    # Вычисляем F1-score
    return f1_score(true_labels, pred_labels)


# Запись результатов в CSV
def save_to_csv(final_results, output_file="submission.csv"):
    final_submission = []
    for result in final_results:
        final_submission.append({
            "file": result["file"],
            "recovery": result["recovery_intervals"],
            "drop": result["drop_intervals"]
        })

    final_submission_df = pd.DataFrame(final_submission)
    final_submission_df.to_csv(output_file, index=False)
    print(f"Результаты сохранены в {output_file}")


# Пример использования
if __name__ == "__main__":
    final_results = []

    data = pd.DataFrame({
        "Время (часы)": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Давление (атм)": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150]
    })

    true_recovery = [[1, 3]]
    true_drop = [[5, 7]]
    recovery_intervals = [[1, 3]]
    drop_intervals = [[5, 7]]

    f1_recovery = calculate_f1_score(true_recovery, recovery_intervals, data)
    f1_drop = calculate_f1_score(true_drop, drop_intervals, data)

    print("F1-score для КВД:", f1_recovery)
    print("F1-score для КПД:", f1_drop)

    # Добавление в список финальных результатов
    final_results.append({
        "file": "example_file.csv",
        "recovery_intervals": recovery_intervals,
        "drop_intervals": drop_intervals,
        "f1_recovery": f1_recovery,
        "f1_drop": f1_drop
    })

    # Сохранение результатов в файл
    save_to_csv(final_results)
