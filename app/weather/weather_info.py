from collections import defaultdict
import os
from app.helper.helper import get_system_time, timestamp_to_datetime
from flask import abort
import requests
import requests
from app.weather import constants
import logging
import datetime
import geocoder

logger = logging.getLogger(__name__)


class WeatherInfo:
    def __init__(self):
        self.api_key = os.getenv(constants.API_KEY_ENV_VAR, None)
        self.city = None
        self.lat = None
        self.lon = None
        self.set_location()


    def set_location(self):
        g = geocoder.ip('me')
        self.coords = g.latlng
        self.lat, self.lon = self.coords[0], self.coords[1]
        reverse_geocode = geocoder.osm(self.coords, method='reverse', headers={'User-Agent': 'Infoboard/1.0'})
        self.city = reverse_geocode.city
        logging.info(f'[*] Got coordinates for city {self.city}: {self.lat}, {self.lon}')

        if self.city is None:
            abort(400, constants.CITY_MISSING)


    def get_weather_info(self):
        current_data = self.get_current_data(constants.CURRENT_API)
        forecast_data = self.get_forecast_data(constants.FORECAST_API)

        return current_data, forecast_data


    def get_data(self, url):
        if self.api_key is None:
            abort(400, constants.API_KEY_MISSING)

        url = url.format(self.lat, self.lon, self.api_key)
        weather_data = requests.get(url).json()
        logging.debug(f'[*] Got weather data for city {self.city}: {weather_data}')
        return weather_data


    def get_current_data(self, url):
        weather_data = self.get_data(url)
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


    def get_forecast_data(self, url):
        weather_data = self.get_data(url)
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
                constants.TIME: datetime.datetime.strptime(forecast.get('dt_txt'), '%Y-%m-%d %H:%M:%S').strftime('%H:%M'),
                constants.WEATHER_FORECAST_DESCRIPTION: constants.WEATHER_DESCRPITION_MAPPING.get(forecast.get('weather')[0].get('description'), ''),
                constants.WEATHER_FORECAST_ICON: forecast.get('weather')[0].get('icon'),
                constants.PROP_PRECIPITATION: float(forecast.get('pop')),
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
