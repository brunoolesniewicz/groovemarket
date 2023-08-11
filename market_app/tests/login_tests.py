import pytest
from market_app.forms import LoginForm


@pytest.mark.django_db
def test_login_page_view_get(client):
    response = client.get('/login/')
    assert response.status_code == 200
    assert 'form' in response.context
    assert issubclass(response.context['form'], LoginForm)


@pytest.mark.django_db
def test_login_page_view_post_valid(client, user1):
    response = client.post('/login/', {'username': user1.username, 'password': 'testpassword1'})
    assert response.status_code == 302
    assert response.url == '/'


@pytest.mark.django_db
def test_login_page_view_post_invalid(client, user1):
    response = client.post('/login/', {'username': user1.username, 'password': 'invalidpassword'})
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'Nieprawidłowa nazwa użytkownika lub hasło.' in response.context['form'].errors['__all__']
