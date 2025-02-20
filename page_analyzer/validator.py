from validators.url import url as validate
from urllib.parse import urlparse


def validate_url(url: str) -> str:
    if not url:
        return 'Введите URL'
    if len(url) > 255:
        return 'URL превышает 255 символов'
    if not validate(url):
        return 'Некорректный URL'
    return 'OK'


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}'.lower()
