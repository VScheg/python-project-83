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
from page_analyzer.html_parser import get_seo
from page_analyzer.repo import UrlRepository, CheckRepository


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


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
    url_repo = UrlRepository(DATABASE_URL)
    data = request.form.to_dict()
    urls_data = url_repo.show_urls()
    url = data.get('url')
    if validate_url(url):
        normalized_url = normalize_url(url)
        for item in urls_data:
            if normalized_url == item.url:
                id = url_repo.get_url_id(normalized_url)
                flash('Страница уже существует', 'info')
                break
        else:
            id = url_repo.add_url(normalized_url)
            flash('Страница успешно добавлена', 'success')

        return redirect(url_for('show_info', id=id))
    else:
        flash('Некорректный URL', 'danger')
        return render_template('base/index.html'), 422


@app.route('/urls/<int:id>', methods=['GET', 'POST'])
def show_info(id: int):
    url_repo = UrlRepository(DATABASE_URL)
    url_info = url_repo.url_info(id)

    if url_info is None:
        return render_template('404.html'), 404

    check_repo = CheckRepository(DATABASE_URL)
    checks = check_repo.show_checks(id)
    return render_template('show.html', url_info=url_info, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def add_check(id: int):
    """
    Check the url,
    if no exceptions, add results of the check to the database,
    show page with url and checks information,
    flash messages depending on presence of exceptions.
    """
    try:
        url_repo = UrlRepository(DATABASE_URL)
        url = url_repo.get_url(id)
        url_check = get_seo(url)
        check_repo = CheckRepository(DATABASE_URL)
        check_repo.add_check(url_check, id)
        flash('Страница успешно проверена', 'success')
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('show_info', id=id))


@app.route('/urls')
def show_urls():
    url_repo = UrlRepository(DATABASE_URL)
    urls = url_repo.show_urls()
    return render_template('index.html', urls=urls)
