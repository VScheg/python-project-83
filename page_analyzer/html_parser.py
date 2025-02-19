import requests
from bs4 import BeautifulSoup


def get_seo(url: str) -> dict[str, str | int]:
    """
    Gets from url HTML page and returns SEO parameters - h1, title, description and status code of page.
    """
    response = requests.get(url)
    response.raise_for_status()
    h1, title, description = parse_html(response)
    return {
        'status_code': response.status_code,
        'h1': h1,
        'title': title,
        'description': description,
    }


def parse_html(response: requests.models.Response) -> tuple[str, str, str]:
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

    return h1, title, description
