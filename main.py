from flask import Flask, render_template, url_for, request, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import config
from pyowm import OWM #погода
import pyowm
import os
import parser_service


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gomel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

owm = OWM(config.WEATHER_TOKEN) #инициализация класса OWM
mgr = owm.weather_manager()
observation_gomel = mgr.weather_at_place('Gomel,BY')
w = observation_gomel.weather


@app.route('/')
def index():
    ''' Функция для отображения главной страницы сайта '''
    weather_on_city = 'Температура по городу - ' + str(w.temperature('celsius')['temp']) + '°C'
    weather_on_city_center = 'В центре - ' + str(w.temperature('celsius')['feels_like']) + '°C'
    sunrise = 'Восход - ' + datetime.fromtimestamp(w.sunrise_time('unix')).strftime("%H:%M")
    sunset = 'Закат -  ' + str(datetime.fromtimestamp(w.sunset_time('unix')).strftime("%H:%M"))
    wind_speed = '\nСкорость ветра - ' + str(w.wind()['speed']) +  'м/с'
    avarage_salary_in_this_month = parser_service.get_avarage_salary_in_this_month()
    avarage_salary_in_prev_month = parser_service.get_avarage_salary_in_prev_month()
    population = parser_service.get_gomel_population()

    if parser_service.get_trand_salary() == True:
        trand = '↗'
        color = '#0c0'
    else:
        trand = '↘'
        color = '#F70000'

    return render_template('index.html', weather_on_city = weather_on_city,
                                         weather_on_city_center = weather_on_city_center,
                                         sunrise = sunrise,
                                         sunset = sunset,
                                         wind_speed = wind_speed,
                                         avarage_salary = avarage_salary_in_this_month,
                                         avarage_salary_in_prev_month = avarage_salary_in_prev_month,
                                         trand = trand,
                                         color = color,
                                         population = population
                                         )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/photo')
def all_photos():
    ''' Отображения всех фотографйи на сайте  '''
    return render_template('photo.html')


@app.route('/upload_photo', methods=['POST','GET'])
def upload_photo():
    ''' Отображения формы для загрузки фотографии на модерацию  '''
    return render_template('upload_photo.html')






if __name__ == "__main__":
    app.run(debug=True)
