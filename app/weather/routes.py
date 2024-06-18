import os
from flask import abort, jsonify, render_template, request
import requests
from app.main import bp
import requests
from app.weather import constants
import logging
from geopy.geocoders import Nominatim
import datetime

logger = logging.getLogger(__name__)


FORECAST_API = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric'
CURRENT_API = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric'
WEATHER_ICON_URL = 'https://openweathermap.org/img/w/{}.png'
API_KEY = os.getenv(constants.API_KEY_ENV_VAR, None)
CITY = 'Karlsruhe'


def timestamp_to_datetime(timestamp, timezone):
    utc_dt = datetime.datetime.utcfromtimestamp(timestamp)
    timezone_offset = datetime.timedelta(seconds=timezone)
    return (utc_dt + timezone_offset).strftime('%-H:%M')

def get_data(url, city):
    if API_KEY is None:
        abort(400, constants.API_KEY_MISSING)

    coords = get_coordinates(city).json
    lat, long = coords.get(constants.LATITUDE, None), coords.get(constants.LONGITUDE, None)
    logging.info(f'[*] Got coordinates for city {city}: {lat}, {long}')

    url = url.format(lat, long, API_KEY)
    weather_data = requests.get(url).json()
    logging.debug(f'[*] Got weather data for city {city}: {weather_data}')
    return weather_data


def get_current_data(url, city):
    weather_data = get_data(url, city)
    time_zone = int(weather_data.get('timezone'))
    return {
        constants.TIME: timestamp_to_datetime(
            weather_data.get('dt'), time_zone
        ),
        constants.WEATHER_FORECAST_DESCRIPTION: weather_data.get('weather')[0].get('description'),
        constants.WEATHER_FORECAST_ICON: weather_data.get('weather')[0].get('icon'),
        constants.TEMP: int(weather_data.get('main').get('temp')),
    }


def get_forecast_data(url, city):
    weather_data = get_data(url, city)
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
    for i, forecast in enumerate(weather_data.get('list')):
        if i == 8: break
        specific_weather_data.get(constants.FORECASTS).append({
            constants.TIME: datetime.datetime.strptime(forecast.get('dt_txt'), '%Y-%m-%d %H:%M:%S').strftime('%-H'),
            constants.WEATHER_FORECAST_DESCRIPTION: forecast.get('weather')[0].get('description'),
            constants.WEATHER_FORECAST_ICON: forecast.get('weather')[0].get('icon'),
            constants.PROP_PRECIPITATION: int(float(forecast.get('pop')) * 100),
            constants.TEMP: int(forecast.get('main').get('temp')),
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

    current_data = get_current_data(CURRENT_API, city)
    print(current_data)
    forecast_data = get_forecast_data(FORECAST_API, city)
    return render_template('weather.html', weather_data=forecast_data, current_data=current_data)
