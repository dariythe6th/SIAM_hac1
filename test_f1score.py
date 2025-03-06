import unittest
import pandas as pd
import numpy as np
from f1score import calculate_f1_score

class TestCalculateF1Score(unittest.TestCase):
    def setUp(self):
        # Создаем синтетические данные для тестирования
        self.data = pd.DataFrame({
            "Время (часы)": np.arange(0, 1000, 10),
            "Давление (атм)": np.random.rand(100) * 100
        })

    def test_calculate_f1_score_perfect_match(self):
        # Проверяем случай, когда интервалы идеально совпадают
        true_intervals = [[100, 300]]
        pred_intervals = [[100, 300]]
        f1 = calculate_f1_score(true_intervals, pred_intervals, self.data)
        self.assertAlmostEqual(f1, 1.0)  # F1-score должен быть равен 1

    def test_calculate_f1_score_no_match(self):
        # Проверяем случай, когда интервалы не совпадают
        true_intervals = [[100, 300]]
        pred_intervals = [[400, 600]]
        f1 = calculate_f1_score(true_intervals, pred_intervals, self.data)
        self.assertAlmostEqual(f1, 0.0)  # F1-score должен быть равен 0

    def test_calculate_f1_score_partial_match(self):
        # Проверяем случай частичного совпадения интервалов
        true_intervals = [[100, 300]]
        pred_intervals = [[200, 400]]
        f1 = calculate_f1_score(true_intervals, pred_intervals, self.data)
        self.assertTrue(0 < f1 < 1)  # F1-score должен быть между 0 и 1

if __name__ == "__main__":
    unittest.main()