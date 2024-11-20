import os
from flask import Flask
from app.main import bp as main_bp
from app.weather import bp as weather_bp
from app.config import Config, DevelopmentConfig
import logging


def create_app():
    app = Flask(__name__)
    if os.getenv('FLASK_ENV') == 'test':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(Config)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('[*] Starting application')

    app.register_blueprint(main_bp)

    app.register_blueprint(weather_bp)

    return app
