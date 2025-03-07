import numpy as np
import pandas as pd

# Создаем массив времени с шагом 0.5 часа от 0 до 30 часов
time = np.arange(0, 30.5, 0.5)

# Инициализируем давление базовым значением 100
pressure = np.full_like(time, 100.0, dtype=float)

# Интервал КВД: увеличение давления от 5 до 7 часов
mask_recovery = (time >= 5) & (time <= 7)
pressure[mask_recovery] = np.linspace(100, 140, np.sum(mask_recovery))

# Интервал КПД: снижение давления от 15 до 17 часов
mask_drop = (time >= 15) & (time <= 17)
pressure[mask_drop] = np.linspace(140, 100, np.sum(mask_drop))

# Создаем DataFrame и сохраняем в CSV
df = pd.DataFrame({"Время (часы)": time, "Давление (атм)": pressure})
df.to_csv("sample_data.csv", index=False)

print("Файл sample_data.csv успешно создан.")
