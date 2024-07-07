import pytest
from flask_wiki.test.conftest import get_app_urls

def test_available_urls(get_app_urls, test_client):
    urls = get_app_urls
    client = test_client
    not_200 = {}
    status_200 = {}
    for url in urls:
        response = client.get(url)
        if response.status_code != 200:
            not_200[url] = response.status_code
        else:
            status_200[url] = response.status_code

    assert len(not_200) == 0, (f"All urls: {len(urls)}. \n Not available url  {not_200} "
                               f"\n Available urls: {status_200}")
