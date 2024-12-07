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
    """ Ищет ключ города по названию, с помощью которого будем получать прогнозы """
    res = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search', params={
        'apikey': api_key,
        'q': city,
        'language': 'ru-ru'
    }).json()
    return f'{res[0]["Key"]}'

def get_forecast(api_key, city_key):
    res = requests.get(f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{city_key}', params={
        'apikey': api_key,
        'language': 'ru-ru',
        'details': True,
        'metric': True
    }).json()
    with open('data/forecast.json', 'w') as file:
        json.dump(res, file)

if __name__ == '__main__':
    # app.run(debug=True)
    API_KEY = 'fX0YccRpvIqqAJyDbwsBEtDop7OGrCbn'
    city_key = get_key_by_city(API_KEY, 'Москва')
    get_forecast(API_KEY, city_key)



