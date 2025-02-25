from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
)

import os
from dotenv import load_dotenv

from page_analyzer.validator import validate_url, normalize_url
from page_analyzer.html_parser import parse_html
from page_analyzer.repo import UrlRepository, CheckRepository

import requests


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('base/index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/urls', methods=['POST'])
def url_post():
    """
    Get url from user,
    validate and normalize url,
    add to database if needed,
    redirect to url page if url validated,
    flash messages depending on url validation and presence in database.
    """
    data = request.form.to_dict()
    url = data.get('url')
    error = validate_url(url)
    if error:
        flash(error, 'danger')
        return render_template('base/index.html'), 422

    normalized_url = normalize_url(url)
    if (id := UrlRepository.get_url_id(normalized_url)):
        flash('Страница уже существует', 'info')
    else:
        id = UrlRepository.add_url(normalized_url)
        flash('Страница успешно добавлена', 'success')

    return redirect(url_for('show_info', id=id))


@app.route('/urls/<int:id>', methods=['GET', 'POST'])
def show_info(id: int):
    url_info = UrlRepository.url_info(id)

    if url_info is None:
        return render_template('404.html'), 404

    checks = CheckRepository.show_checks(id)
    return render_template('show.html', url_info=url_info, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def add_check(id: int):
    """
    Check the url,
    if no exceptions, add results of the check to the database,
    show page with url and checks information,
    flash messages depending on presence of exceptions.
    """
    url = UrlRepository.get_url(id)
    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    else:
        url_check = parse_html(response)
        CheckRepository.add_check(url_check, id)
        flash('Страница успешно проверена', 'success')

    return redirect(url_for('show_info', id=id))


@app.route('/urls')
def show_urls():
    urls = UrlRepository.show_urls()
    return render_template('index.html', urls=urls)
