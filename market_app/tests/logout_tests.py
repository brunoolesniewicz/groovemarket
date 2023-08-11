import pytest


@pytest.mark.django_db
def test_logout_view(client, user1):
    client.login(username=user1.username, password='testpassword1')

    assert user1.is_authenticated

    response = client.get('/logout/')

    assert response.status_code == 302
    assert response.url == '/'

    response = client.get('/')

    assert not response.context['user'].is_authenticated
