from collections import defaultdict
import os
import time
from flask import abort
import requests
import requests
from app.weather import constants
import logging
import datetime
from geopy.geocoders import Nominatim

logger = logging.getLogger(__name__)


API_KEY = os.getenv(constants.API_KEY_ENV_VAR, None)


def timestamp_to_datetime(timestamp, timezone):
    utc_dt = datetime.datetime.utcfromtimestamp(timestamp)
    timezone_offset = datetime.timedelta(seconds=timezone)
    return (utc_dt + timezone_offset).strftime('%-H:%M')

def get_system_time():
    return datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y").strftime('%-H:%M')


def get_data(url, city):
    if API_KEY is None:
        abort(400, constants.API_KEY_MISSING)

    coords = get_coordinates(city)
    lat, long = coords.get(constants.LATITUDE, None), coords.get(constants.LONGITUDE, None)
    logging.info(f'[*] Got coordinates for city {city}: {lat}, {long}')

    url = url.format(lat, long, API_KEY)
    weather_data = requests.get(url).json()
    logging.debug(f'[*] Got weather data for city {city}: {weather_data}')
    return weather_data


def get_current_data(url, city):
    weather_data = get_data(url, city)
    now = datetime.datetime.now()
    return {
        constants.DATE: now.strftime('%d %b'),
        constants.DAY: now.strftime("%A"),
        constants.CITY: weather_data.get('name'),
        constants.TIME: get_system_time(),
        constants.WEATHER_FORECAST_DESCRIPTION: constants.WEATHER_DESCRPITION_MAPPING.get(weather_data.get('weather')[0].get('description'), ''),
        constants.WEATHER_FORECAST_ICON: weather_data.get('weather')[0].get('icon'),
        constants.TEMP: int(weather_data.get('main').get('temp')),
        constants.TEMP_MIN: int(weather_data.get('main').get('temp_min')),
        constants.TEMP_MAX: int(weather_data.get('main').get('temp_max')),
        constants.HUMIDITY: int(weather_data.get('main').get('humidity')),
        constants.WIND: int(weather_data.get('wind').get('speed')),
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
        constants.DAILY_FORECASTS: [],
    }
    for i, forecast in enumerate(weather_data.get('list')):
        if i == 8: break
        specific_weather_data.get(constants.FORECASTS).append({
            constants.TIME: datetime.datetime.strptime(forecast.get('dt_txt'), '%Y-%m-%d %H:%M:%S').strftime('%-H'),
            constants.WEATHER_FORECAST_DESCRIPTION: constants.WEATHER_DESCRPITION_MAPPING.get(forecast.get('weather')[0].get('description'), ''),
            constants.WEATHER_FORECAST_ICON: forecast.get('weather')[0].get('icon'),
            constants.PROP_PRECIPITATION: int(float(forecast.get('pop')) * 100),
            constants.TEMP: int(forecast.get('main').get('temp')),
        })

    daily_max_temps = defaultdict(lambda: {constants.TEMP: float('-inf'), constants.WEATHER_FORECAST_ICON: None})
    for forecast in weather_data["list"]:
        date = datetime.datetime.fromtimestamp(forecast["dt"]).strftime('%a')
        temp = int(forecast["main"]["temp"])
        icon = forecast["weather"][0]["icon"]
        if temp > daily_max_temps[date][constants.TEMP]:
            daily_max_temps[date] = {constants.TEMP: temp, constants.WEATHER_FORECAST_ICON: icon}
    specific_weather_data.get(constants.DAILY_FORECASTS).append(dict(daily_max_temps))

    return specific_weather_data


def get_coordinates(city):
    geolocator = Nominatim(user_agent='raspiledisplay')

    if not city:
        abort(400, constants.COORDS_CITY_MISSING)

    location = geolocator.geocode(city)
    if location:
        return {
            constants.CITY: city,
            constants.LATITUDE: location.latitude,
            constants.LONGITUDE: location.longitude
        }
    else:
        return abort(400, constants.COORDS_CITY_NOT_FOUND)
