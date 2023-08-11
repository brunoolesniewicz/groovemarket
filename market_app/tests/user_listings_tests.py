import pytest
from market_app.forms import CreateConversationForm
from market_app.models import UsersFollows, Conversations


@pytest.mark.django_db
def test_user_listings_view_get(authenticated_user1, user2, user2_listing, user1_follows_user2):
    response = authenticated_user1.get(f'/user/{user2.username}/')

    assert response.status_code == 200
    assert 'listings' in response.context
    assert len(response.context['listings']) == 1
    assert 'user' in response.context
    assert 'user_listings_count' in response.context
    assert 'followers_count' in response.context
    assert 'following_count' in response.context
    assert 'user_followed' in response.context
    assert 'conversation_form' in response.context
    assert 'conversation' in response.context
    assert isinstance(response.context['conversation_form'], CreateConversationForm)


@pytest.mark.django_db
def test_user_listings_view_post_follow_unfollow(authenticated_user1, user1, user2, user1_follows_user2):
    response = authenticated_user1.get(f'/user/{user2.username}/')

    assert response.context['followers_count'] == 1
    assert response.context['following_count'] == 0
    assert UsersFollows.objects.filter(follower=user1, following=user2).exists()

    response = authenticated_user1.post(f'/user/{user2.username}/', {"follow_unfollow": ""})

    assert response.status_code == 302
    assert not UsersFollows.objects.filter(follower=user1, following=user2).exists()

    response = authenticated_user1.get(f'/user/{user2.username}/')

    assert response.context['followers_count'] == 0
    assert response.context['following_count'] == 0


@pytest.mark.django_db
def test_user_listings_view_post_create_conversation(authenticated_user1, user1, user2):
    client = authenticated_user1

    response = client.get(f"/user/{user2.username}/")
    assert response.status_code == 200
    assert not Conversations.objects.filter(sender=user1, receiver=user2, listing=None).exists()


@pytest.mark.django_db
def test_user_listings_view_post_existing_conversation(authenticated_user1, user1, user2, user1_user2_conversation_no_listing):
    client = authenticated_user1

    response = client.get(f"/user/{user2.username}/")
    assert response.status_code == 200
    assert Conversations.objects.filter(sender=user1, receiver=user2, listing=None).exists()
