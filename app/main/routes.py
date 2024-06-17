from app.main import bp
from app.weather.routes import get_weather


@bp.route('/', methods=['GET'])
def index():
    return get_weather()
