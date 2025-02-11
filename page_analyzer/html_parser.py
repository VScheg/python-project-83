import requests
from bs4 import BeautifulSoup


def parse_html(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    h1 = soup.find('h1').text if soup.find('h1') else ''
    title = soup.title.string if soup.title else ''
    description = soup.find(
        'meta',
        attrs={'name': 'description'}
    )['content'] if soup.find(
        'meta',
        attrs={'name': 'description'}
    ) else ''

    result = {
        'status_code': response.status_code,
        'h1': h1,
        'title': title,
        'description': description,
    }
    return result
