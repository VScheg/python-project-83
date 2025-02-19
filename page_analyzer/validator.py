from validators.url import url as validate
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    return True if url and validate(url) and len(url) < 256 else False


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}'.lower()
