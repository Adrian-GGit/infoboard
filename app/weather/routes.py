import os
from flask import abort, jsonify, request
import requests
from app.main import bp
import requests
from app.weather import constants
import logging
from geopy.geocoders import Nominatim
import datetime

logger = logging.getLogger(__name__)


# { "cod": 429,
# "message": "Your account is temporary blocked due to exceeding of requests limitation of your subscription type. 
# Please choose the proper subscription http://openweathermap.org/price"
# }

FORECAST_API = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'
CURRENT_API = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'
WEATHER_ICON_URL = 'https://openweathermap.org/img/w/{}.png'
API_KEY = os.getenv(constants.API_KEY_ENV_VAR, None)
CITY = 'Karlsruhe'


def timestamp_to_datetime(timestamp, timezone):
    utc_dt = datetime.datetime.utcfromtimestamp(timestamp)
    timezone_offset = datetime.timedelta(seconds=timezone)
    return (utc_dt + timezone_offset).strftime('%H:%M:%S')


def get_data(url, city, url_params=None):
    if API_KEY is None:
        abort(400, constants.API_KEY_MISSING)

    coords = get_coordinates(city).json
    lat, long = coords.get(constants.LATITUDE, None), coords.get(constants.LONGITUDE, None)
    logging.info(f'[*] Got coordinates for city {city}: {lat}, {long}')

    url = url.format(lat, long, API_KEY)
    weather_data = requests.get(url).json()
    logging.debug(f'[*] Got weather data for city {city}: {weather_data}')
    time_zone = int(weather_data.get('city').get('timezone'))

    specific_weather_data = {
        constants.SUNRISE: timestamp_to_datetime(
            weather_data.get('city').get('sunrise'), time_zone
        ),
        constants.SUNSET: timestamp_to_datetime(
            weather_data.get('city').get('sunset'), time_zone
        ),
        constants.FORECASTS: [],
    }
    for forecast in weather_data.get('list'):
        specific_weather_data.get(constants.FORECASTS).append({
            constants.TEMP_MIN: forecast.get('main').get('temp_min'),
            constants.TEMP_MAX: forecast.get('main').get('temp_max'),
            constants.WEATHER_FORECAST_ID: forecast.get('weather')[0].get('id'),
            constants.WEATHER_FORECAST_DESCRIPTION: forecast.get('weather')[0].get('description'),
            constants.WEATHER_FORECAST_ICON: forecast.get('weather')[0].get('icon'),
            constants.TEMP_FEELS_LIKE: forecast.get('main').get('feels_like'),
            constants.PROP_PRECIPITATION: forecast.get('pop'),
            constants.TEMP: forecast.get('main').get('temp'),
        })

    return specific_weather_data


@bp.route('/get_coordinates', methods=['GET'])
def get_coordinates(city):
    geolocator = Nominatim(user_agent='raspiledisplay')

    city_name = request.args.get(constants.CITY) or city
    if not city_name:
        abort(400, constants.COORDS_CITY_MISSING)

    location = geolocator.geocode(city_name)
    if location:
        return jsonify({
            constants.CITY: city_name,
            constants.LATITUDE: location.latitude,
            constants.LONGITUDE: location.longitude
        })
    else:
        return abort(400, constants.COORDS_CITY_NOT_FOUND)


@bp.route('/forecast', methods=['GET'])
def get_weather():
    city = request.args.get(constants.CITY, CITY)
    if city is None:
        abort(400, constants.CITY_MISSING)

    return get_data(FORECAST_API, city)
