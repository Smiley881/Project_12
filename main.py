import requests, json
from flask import Flask, render_template, request
from get_weather import *

app = Flask(__name__)
API_KEY = 'fX0YccRpvIqqAJyDbwsBEtDop7OGrCbn'

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    else:
        # Сохранение данных в json файле
        city_start = request.form['city_start']
        city_end = request.form['city_end']
        city_start_key = get_key_by_city(API_KEY, city_start)
        city_end_key = get_key_by_city(API_KEY, city_end)
        get_forecast(API_KEY, city_start_key)
        get_forecast(API_KEY, city_end_key)
        day_forecast = int(request.form['forecast_day'])
        _, metrics_start, __ = check_bad_weather(city_start_key, day_forecast)
        advices, metrics_end, points = check_bad_weather(city_end_key, day_forecast)

        if points < 9:
            result = 'В точке назначения благоприятные погодные условия'
        elif 9 <= points < 19:
            result = 'В точке назначения не очень благоприятные погодные условия'
        elif 19 < points < 29:
            result = 'В точке назначения наблюдаются значительные неблагоприятные условия'
        else:
            result = 'Крайне не советуем ехать в точку назначения в ближайшее время'
    return render_template('result.html',
                           city_start=city_start,
                           city_end=city_end,
                           temp_start=metrics_start['temp'],
                           hum_start=metrics_start['hum'],
                           speed_wind_start=metrics_start['speed_wind'],
                           rain_start=metrics_start['rain'],
                           snow_start=metrics_start['snow'],
                           temp_end=metrics_end['temp'],
                           hum_end=metrics_end['hum'],
                           speed_wind_end=metrics_end['speed_wind'],
                           rain_end=metrics_end['rain'],
                           snow_end=metrics_end['snow'],
                           advices=advices,
                           result=result
                           )

if __name__ == '__main__':
    app.run(debug=True)



