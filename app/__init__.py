from flask import Flask
from app.main import bp as main_bp
from app.weather import bp as weather_bp
from config import Config
import logging



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('[*] Starting application')

    app.register_blueprint(main_bp)

    app.register_blueprint(weather_bp)

    return app
