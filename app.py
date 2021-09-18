# app.py

import json_logging
import logging
import os
import sys
import os.path

from PIL import Image
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
# настройки json-логирования
json_logging.ENABLE_JSON_LOGGING = True
json_logging.init(framework_name='flask')
json_logging.init_request_instrument(app)

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))  # вывод json-логирования

UPLOAD_FOLDER = './static/upload'  # директория сохранения картинки

app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # максимальный объём содержимого файла в запросе

ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg'}  # допустимый формат


# исключение по формату файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# подсчёт белого и черного цветов
def data_image(pix, width, height):
    count_black = 0
    count_white = 0
    for x in range(width):
        for y in range(height):
            a = pix[x, y][0]
            b = pix[x, y][1]
            c = pix[x, y][2]
            if a == 0 and b == 0 and c == 0:
                count_black += 1
            elif a == 255 and b == 255 and c == 255:
                count_white += 1
    if count_black > count_white:
        mess = 'черных пикселей больше'
    elif count_black < count_white:
        mess = 'белых пикселей больше'
    elif (count_black > 0) and (count_white > 0) and (count_white == count_black):
        mess = 'количество пикселей белого и черного цветов равно'
    elif count_black == 0 and count_white == 0:
        mess = 'пиксели белого и черного цветов отсутствуют'

    return mess


# подсчёт пикселей по заданному hex-коду
def color(pix, width, height, hex_code):
    a = '0x' + hex_code[:2]
    a = int(a, 0)
    b = '0x' + hex_code[2:4]
    b = int(b, 0)
    c = '0x' + hex_code[4:]
    c = int(c, 0)
    dec_val = (a, b, c)
    print(dec_val)
    count_color = 0
    for x in range(width):
        for y in range(height):
            a1 = pix[x, y][0]
            b1 = pix[x, y][1]
            c1 = pix[x, y][2]
            if a1 == a and b1 == b and c1 == c:
                count_color += 1
            else:
                continue
    return count_color


# главная страница
@app.route('/')
def home():
    logger.info("log statement")
    return render_template('index.html', title="Загрузка картинки", title2="Выберете файл для загрузки")


# загрузка картинки
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    global pix, width, height  # глобальные переменные: пиксели, ширина, высота картинки
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = Image.open(file)
        mode = image.getbands()
        if mode == ('R', 'G', 'B') or mode == ('R', 'G', 'B', 'A'):
            width = image.size[0]
            height = image.size[1]
            pix = image.load()
            mess = data_image(pix, width, height)
            logger.info("log statement")
            return render_template('index.html', filename=filename, title="Картинка загружена", colour_wb=mess)
        else:
            mess_err = 'Данный режим не поддерживается, поддерживается RGB и RGBA'
            logger.info("log statement")
            return render_template('index.html', title="Загрузка картинки", title2="Выберите файл для загрузки",
                                   err_form=mess_err)
    else:
        mess_err = 'Неверный формат файла, выберете файл c расширением: webp, png, jpg, jpeg, gif'
        logger.info("log statement")
        return render_template('index.html', title="Загрузка картинки", title2="Выберете файл для загрузки",
                               err_form=mess_err)


# отображение картинки
@app.route('/display/<filename>')
def display_image(filename):
    logger.info("log statement")
    return redirect(url_for('static', filename='upload/' + filename), code=301)


# вывод-подчёт пикселей по заданному hex коду
@app.route('/index', methods=['GET', 'POST'])
def hex_color():
    hex_code = request.form['hex']
    count_color = color(pix, width, height, hex_code)
    logger.info("test log statement")
    return render_template('index.html', count_color=f'Количество пикселей заданного цвета: {count_color}',
                           title="", title2="")


# начало
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
