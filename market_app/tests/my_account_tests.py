import pytest


@pytest.mark.django_db
def test_my_account_view_unauthenticated(client):
    response = client.get('/my_account/')
    assert response.status_code == 302
    assert response.url.startswith('/login/')


@pytest.mark.django_db
def test_my_account_view_authenticated(authenticated_user1, user1, user1_listing, user1_follows_user2):
    response = authenticated_user1.get('/my_account/')
    assert response.status_code == 200
    assert 'user' in response.context
    assert 'user_listings_count' in response.context
    assert 'followers_count' in response.context
    assert 'following_count' in response.context
    assert response.context['user'] == user1
    assert response.context['user_listings_count'] == 1
    assert response.context['followers_count'] == 0
    assert response.context['following_count'] == 1


@pytest.mark.django_db
def test_my_account_view_post_delete_avatar(authenticated_user1, user1):
    response = authenticated_user1.post('/my_account/', {'delete_avatar': ''})
    assert response.status_code == 302
    assert response.url == '/my_account/'

    user1.refresh_from_db()
    assert user1.avatar == 'default_avatar.jpg'
