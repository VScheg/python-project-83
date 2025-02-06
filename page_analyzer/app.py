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

from page_analyzer.url_repo import UrlRepository
from validators.url import url as validate
from urllib.parse import urlparse


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

repo = UrlRepository(DATABASE_URL)


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('base/index.html', messages=messages)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def normalize_url(url):
    parsed = urlparse(url)
    return parsed.scheme + '://' + parsed.netloc


@app.route('/', methods=['POST'])
def url_post():
    data = request.form.to_dict()
    urls_data = repo.show_urls()
    url = data.get('url')
    if validate(url):
        normalized_url = normalize_url(url)
        for item in urls_data:
            if normalized_url == item.get('url'):
                id = repo.get_url_id(normalized_url)
                flash('Страница уже существует', 'info')
                break
        else:
            id = repo.add_url(normalized_url)
            flash('Страница успешно добавлена', 'success')

        return redirect(url_for('show_info', id=id))
    else:
        flash('Некорректный URL', 'danger')
        return redirect(url_for('index'))


@app.route('/urls/<id>', methods=['GET', 'POST'])
def show_info(id):
    try:
        messages = get_flashed_messages(with_categories=True)
        url_info = repo.url_info(id)
        checks = repo.show_checks(id)
        return render_template('show.html', url_info=url_info, checks=checks, messages=messages)
    except:
        return render_template('404.html'), 404


@app.route('/urls/<id>/checks', methods=['POST'])
def url_checks(id):
    try:
        repo.add_check(id)
    except:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('show_info', id=id))


@app.route('/urls')
def show_urls():
    urls = repo.show_urls()
    for url in urls:
        for key, value in url.items():
            if value is None:
                url[key] = ''
    return render_template('index.html', urls=urls)
