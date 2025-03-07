import numpy as np
import pandas as pd

# Создаем массив времени с шагом 1 минута (1/60 часа) от 0 до 30 часов
time = np.arange(0, 30, 1/60)  # 30 часов, шаг 1 минута

# Инициализируем давление базовым значением 100 атм
pressure = np.full_like(time, 100.0, dtype=float)

# Интервал КВД: увеличение давления от 5 до 9 часов (4 часа)
mask_recovery = (time >= 5) & (time <= 9)
pressure[mask_recovery] = np.linspace(100, 140, np.sum(mask_recovery))

# Интервал КПД: снижение давления от 15 до 19 часов (4 часа)
mask_drop = (time >= 15) & (time <= 19)
pressure[mask_drop] = np.linspace(140, 100, np.sum(mask_drop))

# Формируем DataFrame и сохраняем в CSV
df = pd.DataFrame({"Время (часы)": time, "Давление (атм)": pressure})
df.to_csv("sample_dat.csv", index=False)

print("Файл sample_dat.csv успешно создан.")

