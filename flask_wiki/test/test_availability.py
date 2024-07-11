import pytest
from flask_wiki.test.conftest import get_app_urls

ROLE_URLS = ['wiki/quiz/show_results',
             ]
@pytest.mark.skip
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

def login(clien, user):
    return clien.post('/',
                      data={'email': user.email,
                            'password': user.password,
                            'submit': True,
                            'csrf_token': 'test_token'},
                      follow_redirects=True)

@pytest.mark.skip
@pytest.mark.parametrize('url', ROLE_URLS)
def test_available_urs_by_roles(init_database, test_client, url):
    '''надо еще подумать'''
    user = init_database
    response = login(test_client, user)
    assert response.status_code == 200

    response = test_client.get(url)
    #assert response.status_code == 200
    assert response.request.url == response.location


@pytest.mark.skip
@pytest.mark.parametrize('url', ROLE_URLS)
def test_available_urs_by_roles_not_auth(init_database, test_client, url):

    response = test_client.get(url)
    assert response.request.url != response.location
