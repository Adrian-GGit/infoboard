from flask import send_from_directory
from app.main import bp
from app.weather.routes import get_weather


@bp.route('/', methods=['GET'])
def index():
    return get_weather()


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        bp.root_path,
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )
