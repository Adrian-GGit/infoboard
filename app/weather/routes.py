from flask import abort, render_template, request
from app.main import bp
from app.weather import constants
import logging

from app.weather.helper import get_current_data, get_forecast_data

logger = logging.getLogger(__name__)


FORECAST_API = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric'
CURRENT_API = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric'
WEATHER_ICON_URL = 'https://openweathermap.org/img/w/{}.png'
CITY = 'Karlsruhe'


@bp.route('/forecast', methods=['GET'])
def get_weather():
    city = request.args.get(constants.CITY, CITY)
    if city is None:
        abort(400, constants.CITY_MISSING)

    current_data = get_current_data(CURRENT_API, city)
    forecast_data = get_forecast_data(FORECAST_API, city)
    return render_template('weather/weather.html', weather_data=forecast_data, current_data=current_data)
