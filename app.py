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
    """
    Визуализация временных рядов давления и его производной с выделенными интервалами КВД и КПД.
    """
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
        color = recovery_colors[idx % len(recovery_colors)]  # Циклически выбираем цвет
        plt.axvspan(interval[0], interval[1], color=color, alpha=0.3, label=f"КВД {idx+1}" if idx < 3 else "")

    # Отображение интервалов КПД
    for idx, interval in enumerate(drop_intervals):
        color = drop_colors[idx % len(drop_colors)]  # Циклически выбираем цвет
        plt.axvspan(interval[0], interval[1], color=color, alpha=0.3, label=f"КПД {idx+1}" if idx < 3 else "")

    # Настройка графика
    plt.xlabel("Время (часы)")
    plt.ylabel("Давление (атм) / Производная")
    plt.title("Выделение интервалов КВД и КПД")
    plt.legend()
    plt.grid()

    # Преобразование графика в base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Если нажата кнопка "Использовать тестовые данные"
        if 'use_test_data' in request.form:
            # Загружаем тестовые данные из data/well_data.csv
            if os.path.exists(os.path.join("data", "well_data.csv")):
                data = load_data(os.path.join("data", "well_data.csv"))
                recovery_intervals, drop_intervals = detect_patterns(data)
                plot_url = plot_intervals(data, recovery_intervals, drop_intervals)
                return render_template('result.html', plot_url=plot_url, recovery=recovery_intervals, drop=drop_intervals, data=data.to_dict('records'))
            else:
                return "Файл data/well_data.csv не найден!"

        # Если загружен файл
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Сохраняем файл
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Загружаем данные
            data = load_data(file_path)

            # Применяем алгоритм для обнаружения интервалов
            recovery_intervals, drop_intervals = detect_patterns(data)

            # Визуализируем результаты
            plot_url = plot_intervals(data, recovery_intervals, drop_intervals)

            # Передаем график, интервалы и данные в шаблон
            return render_template('result.html', plot_url=plot_url, recovery=recovery_intervals, drop=drop_intervals, data=data.to_dict('records'))
    return render_template('index.html')

def main():
    """
    Основная функция для запуска веб-приложения.
    """
    app.run(debug=True)

if __name__ == '__main__':
    main()