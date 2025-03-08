import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect, url_for
import io
import base64
from werkzeug.utils import secure_filename
from search import detect_patterns

# Инициализация Flask-приложения
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Создаем папку для загрузок, если её нет
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def load_data(file_path):
    """
    Загружает данные из CSV-файла и переименовывает колонки.
    """
    data = pd.read_csv(file_path)
    data.columns = ["Время (часы)", "Давление (атм)"]
    return data

def plot_intervals(data, recovery_intervals, drop_intervals):
    plt.figure(figsize=(12, 6))

    # Построение давления
    plt.plot(data["Время (часы)"], data["Давление (атм)"], label="Давление", color='blue')

    # Вычисление производной
    derivative = np.gradient(data["Давление (атм)"])
    plt.plot(data["Время (часы)"], derivative, label="Производная давления", color='red', linestyle='--')

    # Цвета для интервалов
    recovery_colors = ['green', 'blue', 'orange']
    drop_colors = ['red', 'purple', 'yellow']

    # Отображение интервалов КВД
    for idx, interval in enumerate(recovery_intervals):
        color = recovery_colors[idx % len(recovery_colors)]
        plt.axvspan(interval[0], interval[1], color=color, alpha=0.3, label=f"КВД {idx+1}" if idx < 3 else "")
        # Подпись для КВД
        plt.text((interval[0] + interval[1]) / 2, max(data["Давление (атм)"]), "КВД",
                 color=color, fontsize=12, ha='center', va='bottom')

    # Отображение интервалов КПД
    for idx, interval in enumerate(drop_intervals):
        color = drop_colors[idx % len(drop_colors)]
        plt.axvspan(interval[0], interval[1], color=color, alpha=0.3, label=f"КПД {idx+1}" if idx < 3 else "")
        # Подпись для КПД
        plt.text((interval[0] + interval[1]) / 2, min(data["Давление (атм)"]), "КПД",
                 color=color, fontsize=12, ha='center', va='top')

    # Определение и выделение областей
    time = data["Время (часы)"].values
    pressure = data["Давление (атм)"].values

    # Область 1: Влияние ствола скважины (ВСС)
    wb_start = 0
    wb_end = time[np.argmax(derivative > 1)]  # Примерный конец области ВСС
    plt.axvspan(wb_start, wb_end, color='gray', alpha=0.2, label="Влияние ствола скважины (ВСС)")

    # Область 2: Работа пласта
    ra_start = wb_end
    ra_end = time[np.argmax(derivative < 0.5)]  # Примерный конец области работы пласта
    plt.axvspan(ra_start, ra_end, color='yellow', alpha=0.2, label="Работа пласта")

    # Область 3: Влияние границ
    pc_start = ra_end
    pc_end = time[-1]  # Конец графика
    plt.axvspan(pc_start, pc_end, color='pink', alpha=0.2, label="Влияние границ")

    # Настройка графика
    plt.xlabel("Время (часы)")
    plt.ylabel("Давление (атм) / Производная")
    plt.title("Выделение интервалов КВД, КПД и областей на графике")
    plt.legend()
    plt.grid()

    # Преобразование графика в base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Добавляем производную в данные для таблицы
    data['Производная (атм/час)'] = derivative

    return plot_url, data.to_dict('records')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'use_test_data' in request.form:
            if os.path.exists(os.path.join("data", "well_data.csv")):
                data = load_data(os.path.join("data", "well_data.csv"))
                recovery_intervals, drop_intervals = detect_patterns(data)
                plot_url, data_with_derivative = plot_intervals(data, recovery_intervals, drop_intervals)
                return render_template('result.html', plot_url=plot_url, recovery=recovery_intervals, drop=drop_intervals, data=data_with_derivative)
            else:
                return "Файл data/well_data.csv не найден!"

        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            data = load_data(file_path)
            recovery_intervals, drop_intervals = detect_patterns(data)
            plot_url, data_with_derivative = plot_intervals(data, recovery_intervals, drop_intervals)

            return render_template('result.html', plot_url=plot_url, recovery=recovery_intervals, drop=drop_intervals, data=data_with_derivative)
    return render_template('index.html')

def main():
    """
    Основная функция для запуска веб-приложения.
    """
    app.run(debug=True)

if __name__ == '__main__':
    main()