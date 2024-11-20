import json
from app.weather.weather_info import WeatherInfo
from flask import render_template
from app.main import bp
from app.weather import constants
import logging

logger = logging.getLogger(__name__)


@bp.route('/forecast', methods=['GET'])
def get_weather():
    weather_info = WeatherInfo()
    current_data, forecast_data = weather_info.get_weather_info()
    return render_template(
        'weather/weather.html',
        weather_data=forecast_data,
        current_data=current_data,
        time_weather_data=json.dumps(forecast_data.get(constants.FORECASTS)),
    )
