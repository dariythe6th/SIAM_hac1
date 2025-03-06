import unittest
import pandas as pd
import numpy as np
from search import detect_patterns

class TestDetectPatterns(unittest.TestCase):
    def setUp(self):
        # Создаем синтетические данные для тестирования
        self.data = pd.DataFrame({
            "Время (часы)": np.arange(0, 1000, 10),
            "Давление (атм)": np.sin(np.arange(0, 1000, 10) * 0.1) * 100
        })

    def test_detect_patterns_recovery(self):
        # Проверяем, что функция корректно находит интервалы КВД
        recovery_intervals, drop_intervals = detect_patterns(self.data)
        self.assertIsInstance(recovery_intervals, list)
        self.assertIsInstance(drop_intervals, list)
        self.assertTrue(all(isinstance(interval, list) and len(interval) == 2 for interval in recovery_intervals))

    def test_detect_patterns_drop(self):
        # Проверяем, что функция корректно находит интервалы КПД
        recovery_intervals, drop_intervals = detect_patterns(self.data)
        self.assertTrue(all(isinstance(interval, list) and len(interval) == 2 for interval in drop_intervals))

    def test_detect_patterns_noise(self):
        # Проверяем, что функция корректно обрабатывает шум
        noisy_data = self.data.copy()
        noisy_data["Давление (атм)"] += np.random.normal(0, 5, len(noisy_data))
        recovery_intervals, drop_intervals = detect_patterns(noisy_data, noise_threshold=5.0)
        self.assertTrue(len(recovery_intervals) <= len(self.data) / 100)  # Проверяем, что интервалов не слишком много

if __name__ == "__main__":
    unittest.main()