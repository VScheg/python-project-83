from validators.url import url as validate
from urllib.parse import urlparse


def validate_url(url):
    return True if validate(url) and len(url) < 256 else False


def normalize_url(url):
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}'.lower()
