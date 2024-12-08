import requests, json
from datetime import datetime

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

    with open(f'data/forecast_{city_key}_{datetime.today().date()}', 'w') as file:
        json.dump(res, file)

def check_bad_weather(city_key, day_forecast):
    """ Оценивает погоду в точке назначения и возвращает советы,
    погодные значения и уровень неблагоприятности погоды """
    # Чтение файла с погодой
    with open(f'data/forecast_{city_key}_{datetime.today().date()}') as file:
        content = json.load(file)

    # Вывод погодных метрик и сохранение в словаре
    temp_min = content['DailyForecasts'][day_forecast]['Temperature']['Minimum']['Value']
    temp_max = content['DailyForecasts'][day_forecast]['Temperature']['Maximum']['Value']
    temp_avg = round((temp_max + temp_min) / 2, 2)
    hum_avg = content['DailyForecasts'][0]['Day']['RelativeHumidity']['Maximum']
    speed_wind = content['DailyForecasts'][0]['Day']['Wind']['Speed']['Value']
    rain = content['DailyForecasts'][0]['Day']['Rain']['Value']
    snow = content['DailyForecasts'][0]['Day']['Snow']['Value']

    metrics = {
        'temp': temp_avg,
        'hum': hum_avg,
        'speed_wind': speed_wind,
        'rain': rain,
        'snow': snow
    }

    points = 0
    advices = ''
    count_advices = 0

    # Оценка температуры
    if temp_avg <= -35 or temp_avg >= 40:
        points += 10
        advices += '1. В точке назначения будет экстремальный показатель температуры!\n'
        count_advices += 1
    elif -35 < temp_avg <= -20:
        points += 7
        advices += '1. Заморозки. Одевайте очень теплые пуховики.\n'
        count_advices += 1
    elif -20 < temp_avg <= -5:
        points += 4
        advices += '1. В точке назначения будет прохладно.\n'
        count_advices += 1
    elif 31 > temp_avg >= 25:
        points += 4
        advices += '1. Будет слегка жарковато. Одевайтесь посвободнее.\n'
        count_advices += 1
    elif 40 > temp_avg >= 31:
        points += 8
        advices += '1. В точке назначения будет стоять сильная жара. Не забудьте мини-вентиляторы и головные уборы.\n'
        count_advices += 1

    # Оценка влажности
    if 70 < hum_avg < 85:
        points += 3
        advices += f'{count_advices+1}. Влажность будет чуть выше среднего.\n'
        count_advices += 1
    elif hum_avg >= 85:
        points += 7
        advices += f'{count_advices+1}. Влажность будет значительно выше нормы.\n'
        count_advices += 1
    elif 15 <= hum_avg < 30:
        points += 5
        advices += f'{count_advices+1}. Влажность будет немного ниже нормы.\n'
        count_advices += 1
    elif hum_avg < 15:
        points += 9
        advices += f'{count_advices+1}. Влажность будет значительно ниже нормы.\n'
        count_advices += 1

    # Оценка скорости ветра
    if 30 <= speed_wind < 50:
        points += 4
        advices += f'{count_advices+1}. Скорость ветра будет слегка повышена. Придержите свои шляпы!\n'
        count_advices += 1
    elif 50 <= speed_wind < 70:
        points += 10
        advices += f'{count_advices+1}. Скорость ветра будет значительно выше нормы! Будьте осторожны!\n'
        count_advices += 1
    elif speed_wind >= 70:
        points += 20
        advices += f'{count_advices+1}. Штормовой ветер! Будьте бдительны и держитесь безопасных мест.\n'
        count_advices += 1

    # Оценки снежных осадков
    if 5 <= snow < 19:
        points += 2
        advices += f'{count_advices+1}. В точке назначения будет наблюдаться легкий снегопад.\n'
        count_advices += 1
    elif 19 <= snow < 30:
        points += 5
        advices += f'{count_advices+1}. В точке назначения будет сильный снегопад. Одевайтесь теплее!\n'
        count_advices += 1
    elif 30 <= snow < 50:
        points += 10
        advices += f'{count_advices+1}. Прогнозируется обильный снегопад! Одевайтесь теплее!\n'
        count_advices += 1
    elif snow > 50:
        points += 20
        advices += f'{count_advices+1}. Ожидается снежный ураган!\n'
        count_advices += 1

    # Оценка дождей
    if 3 <= rain < 15:
        points += 4
        advices += f'{count_advices+1}. В точке назначения будет пасмурная погода, возможен дождь.\n'
    elif 15 <= rain < 50:
        points += 8
        advices += f'{count_advices+1}. Прогнозируется сильный дождь. Не забудьте взять с собой зонтик.\n'
    elif rain > 50:
        points += 20
        advices += f'{count_advices+1}. Ожидается очень сильный ливень.\n'

    return advices, metrics, points
