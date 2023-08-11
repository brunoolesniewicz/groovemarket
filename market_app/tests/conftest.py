import pytest
from django.test import Client
from market_app.models import *


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user1():
    return CustomUser.objects.create_user(
        username='testuser1',
        password='testpassword1',
        first_name='Test1',
        last_name='User1',
        email='testuser1@example.com',
        bio='Test Bio1',
        avatar='default_avatar.jpg'
    )


@pytest.fixture
def authenticated_user1(user1):
    client = Client()
    client.login(username=user1.username, password='testpassword1')
    return client


@pytest.fixture
def user2():
    return CustomUser.objects.create_user(
        username='testuser2',
        password='testpassword2',
        first_name='Test2',
        last_name='User2',
        email='testuser2@example.com',
        bio='Test Bio2',
        avatar='default_avatar.jpg'
    )


@pytest.fixture
def user3():
    return CustomUser.objects.create_user(
        username='testuser3',
        password='testpassword3',
        first_name='Test3',
        last_name='User3',
        email='testuser3@example.com',
        bio='Test Bio3',
        avatar='default_avatar.jpg'
    )


@pytest.fixture
def user1_listing(user1):
    return Listings.objects.create(
        seller=user1,
        title='Title1',
        description='Test desc 1',
        category='vinyl',
        price=123.11,
        artist='Test artist',
        genre='rock',
        condition='new',
        slug='title1',
        sold=False
    )


@pytest.fixture
def user2_listing(user2):
    return Listings.objects.create(
        seller=user2,
        title='Title2',
        description='Test desc 2',
        category='cd',
        price=10.10,
        artist='Test artist',
        genre='pop',
        condition='por',
        slug='title2',
        sold=False
    )


@pytest.fixture
def user1_offer_on_user2_listing(user1, user2_listing):
    return Offers.objects.create(
        user=user1,
        listing=user2_listing,
        price=12
    )


@pytest.fixture
def user1_follows_user2(user1, user2):
    return UsersFollows.objects.create(
        follower=user1,
        following=user2
    )


@pytest.fixture
def user1_user2_conversation_no_listing(user1, user2):
    return Conversations.objects.create(
        sender=user1,
        receiver=user2
    )


@pytest.fixture
def user2_user1_conversation_listing1(user1, user2, user1_listing):
    return Conversations.objects.create(
        sender=user2,
        receiver=user1,
        listing=user1_listing
    )


@pytest.fixture
def user2_messages_user1_conversation(user2, user2_user1_conversation_listing1):
    return Messages.objects.create(
        conversation=user2_user1_conversation_listing1,
        sender=user2,
        body='test message'
    )


@pytest.fixture
def user1_likes_user2_listing(user1, user2_listing):
    return UsersLikes.objects.create(
        user=user1,
        listing=user2_listing
    )
