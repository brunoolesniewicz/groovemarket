import pytest


@pytest.mark.django_db
def test_landing_page_view_unauthenticated(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_landing_page_view_authenticated(client, user1):
    client.login(username=user1.username, password=user1.password)
    response = client.get('/')
    assert response.status_code == 200
    assert 'listings' in response.context
    assert 'page' in response.context


@pytest.mark.django_db
def test_landing_page_view_authenticated_with_listings(client, user1, user2, user2_listing, user1_follows_user2):
    client.login(username=user1.username, password='testpassword1')
    response = client.get('/')
    assert response.status_code == 200
    assert 'listings' in response.context
    assert 'page' in response.context
    assert len(response.context['listings']) == 1
