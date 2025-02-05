from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    get_flashed_messages,
)

import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('base/index.html', messages=messages)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
