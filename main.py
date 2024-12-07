import requests, json
from flask import Flask, render_template, request

app = Flask(__name__)

# @app.route('/', methods=['POST', 'GET'])
# def main():
#     if request.method == 'GET':
#         return render_template('main.html')
#     else:
#         print(request.form['city_start'])
#         print(request.form['city_end'])

def get_key_by_city(api_key, city):
    """ Ищет ключ города по названию, с помощью которого будем получать прогноз """
    res = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search', params={
        'apikey': api_key,
        'q': city,
        'language': 'ru-ru'
    }).json()
    return f'{res[0]["Key"]}'

def get_forecast(api_key, city_key):
    """ Записывает в json-файл прогноз погоды на 5 дней на основе ключа города """
    res = requests.get(f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{city_key}', params={
        'apikey': api_key,
        'language': 'ru-ru',
        'details': True,
        'metric': True
    }).json()
    with open(f'data/forecast_{city_key}.json', 'w') as file:
        json.dump(res, file)

def check_bad_weather(city_key, day_forecast):
    with open(f'data/forecast_{city_key}.json') as file:
        content = json.load(file)
    temp_min = content['DailyForecasts'][day_forecast]['Temperature']['Minimum']['Value']
    temp_max = content['DailyForecasts'][day_forecast]['Temperature']['Maximum']['Value']
    temp_avg = round((temp_max + temp_min) / 2, 2)
    hum_avg = content['DailyForecasts'][0]['Day']['RelativeHumidity']['Maximum']
    speed_wind = content['DailyForecasts'][0]['Day']['Wind']['Speed']['Value']
    rain = content['DailyForecasts'][0]['Day']['Rain']['Value']
    snow = content['DailyForecasts'][0]['Day']['Snow']['Value']

    points = 0
    advices = ''
    count_advices = 0

    if temp_avg < -20:
        points += 0.7
        advices += '1. Не забудьте очень теплые пуховики и шапки!'
    if hum_avg

if __name__ == '__main__':
    # app.run(debug=True)
    # API_KEY = 'fX0YccRpvIqqAJyDbwsBEtDop7OGrCbn'
    # city_key = get_key_by_city(API_KEY, 'Москва')
    # get_forecast(API_KEY, city_key)



