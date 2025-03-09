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

def plot_intervals(data, recovery_intervals, drop_intervals, derivative):
    """
    Строит график с интервалами КВД, КПД и областями.
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Построение давления на первой оси
    ax1.plot(data["Время (часы)"], data["Давление (атм)"], label="Давление", color='blue')
    ax1.set_xlabel("Время (часы)")
    ax1.set_ylabel("Давление (атм)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Создание второй оси для производной
    ax2 = ax1.twinx()
    ax2.plot(data["Время (часы)"], derivative, label="Производная давления", color='red', linestyle='--')
    ax2.set_ylabel("Производная (атм/час)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Создание второй оси для производной
    ax2 = ax1.twinx()
    ax2.plot(data["Время (часы)"], derivative, label="Производная давления", color='red', linestyle='--')
    ax2.set_ylabel("Производная (атм/час)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')
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

    # Настройка шкалы на оси X (время)
    plt.xticks(np.arange(0, max(data["Время (часы)"]) + 1, 1))  # Шаг 1 час

    # Настройка графика
    plt.title("Выделение интервалов КВД, КПД и областей на графике")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small', ncol=1)
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url, data.to_dict('records')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'use_test_data' in request.form:
            if os.path.exists(os.path.join("data", "well_data.csv")):
                data = load_data(os.path.join("data", "well_data.csv"))
                recovery_intervals, drop_intervals, derivative = detect_patterns(data)
                plot_url, data_with_derivative = plot_intervals(data, recovery_intervals, drop_intervals, derivative)
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
            recovery_intervals, drop_intervals, derivative = detect_patterns(data)
            plot_url, data_with_derivative = plot_intervals(data, recovery_intervals, drop_intervals, derivative)

            return render_template('result.html', plot_url=plot_url, recovery=recovery_intervals, drop=drop_intervals, data=data_with_derivative)
    return render_template('index.html')

def main():
    """
    Основная функция для запуска веб-приложения.
    """
    app.run(debug=True)

if __name__ == '__main__':
    main()
