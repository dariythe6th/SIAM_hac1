import os
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
    Визуализация временных рядов давления с выделенными интервалами КВД и КПД.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data["Время (часы)"], data["Давление (атм)"], label="Давление", color='blue')

    # Отображение интервалов КВД
    for idx, interval in enumerate(recovery_intervals):
        plt.axvspan(interval[0], interval[1], color='green', alpha=0.3, label="КВД" if idx == 0 else "")

    # Отображение интервалов КПД
    for idx, interval in enumerate(drop_intervals):
        plt.axvspan(interval[0], interval[1], color='red', alpha=0.3, label="КПД" if idx == 0 else "")

    # Настройка графика
    plt.xlabel("Время (часы)")
    plt.ylabel("Давление (атм)")
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
                return render_template('result.html', plot_url=plot_url, recovery=recovery_intervals, drop=drop_intervals)
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

            # Передаем график и интервалы в шаблон
            return render_template('result.html', plot_url=plot_url, recovery=recovery_intervals, drop=drop_intervals)
    return render_template('index.html')

def main():
    """
    Основная функция для запуска веб-приложения.
    """
    app.run(debug=True)

if __name__ == '__main__':
    main()