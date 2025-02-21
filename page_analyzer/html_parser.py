import requests
from bs4 import BeautifulSoup


def parse_html(response: requests.models.Response) -> dict[str, str | int]:
    """
    Returns from HTML page SEO parameters - h1, title, description.
    """
    soup = BeautifulSoup(response.content, 'html.parser')

    h1 = soup.find('h1').text if soup.find('h1') else ''
    title = soup.title.string if soup.title else ''

    description = find_description['content'] if (
        find_description := soup.find(
            'meta',
            attrs={'name': 'description'}
        )
    ) else ''

    return {
        'h1': h1,
        'title': title,
        'description': description,
    }
