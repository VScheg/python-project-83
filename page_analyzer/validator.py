from validators.url import url as validate
from urllib.parse import urlparse


def validate_url(url: str) -> str | None:
    if not url:
        return 'Введите URL'
    if len(url) > 255:
        return 'URL превышает 255 символов'
    if not validate(url):
        return 'Некорректный URL'


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}'.lower()
