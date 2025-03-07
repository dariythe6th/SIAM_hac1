from flask import Flask, request, render_template, redirect, url_for
import os
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from werkzeug.utils import secure_filename

# Импортируем нашу функцию обнаружения интервалов
from search import detect_patterns

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Если папка для загрузок не существует, создаём её
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Проверяем наличие файла в запросе
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Загружаем CSV с данными
            data = pd.read_csv(file_path)
            # Предполагается, что в CSV данные с колонками, которые нужно переименовать
            data.columns = ["Время (часы)", "Давление (атм)"]

            # Применяем алгоритм для обнаружения интервалов
            recovery, drop = detect_patterns(data)

            # Построение графика и преобразование в base64
            plt.figure(figsize=(12, 6))
            plt.plot(data["Время (часы)"], data["Давление (атм)"], label="Давление")
            for idx, interval in enumerate(recovery):
                plt.axvspan(interval[0], interval[1], color='green', alpha=0.3,
                            label="КВД" if idx == 0 else "")
            for idx, interval in enumerate(drop):
                plt.axvspan(interval[0], interval[1], color='red', alpha=0.3,
                            label="КПД" if idx == 0 else "")
            plt.xlabel("Время (часы)")
            plt.ylabel("Давление (атм)")
            plt.title("Выделенные интервалы КВД и КПД")
            plt.legend()
            plt.grid()

            img = io.BytesIO()
            plt.savefig(img, format='png')
            plt.close()
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            # Передаем график и интервалы в шаблон
            return render_template('result.html', plot_url=plot_url, recovery=recovery, drop=drop)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
