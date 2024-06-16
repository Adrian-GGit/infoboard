from flask import abort, render_template, request
from app.main import bp
import requests
import logging




@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
