import pytest
from market_app.forms import CreateUserForm
from market_app.models import CustomUser


@pytest.mark.django_db
def test_create_user_view_get(client):
    response = client.get('/register/')
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], CreateUserForm)


@pytest.mark.django_db
def test_create_user_view_post_valid(client):
    data = {
        'username': 'newuser',
        'first_name': 'New',
        'last_name': 'User',
        'email': 'newuser@example.com',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
    }
    response = client.post('/register/', data)
    assert response.status_code == 302
    assert CustomUser.objects.filter(username='newuser').exists()


@pytest.mark.django_db
def test_create_user_view_post_existing_username(client, user1):
    data = {
        'username': user1.username,
        'first_name': 'New',
        'last_name': 'User',
        'email': 'newuser@example.com',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
    }
    response = client.post('/register/', data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'username' in response.context['form'].errors


@pytest.mark.django_db
def test_create_user_view_post_mismatched_passwords(client):
    data = {
        'username': 'newuser',
        'first_name': 'New',
        'last_name': 'User',
        'email': 'newuser@example.com',
        'password1': 'testpassword123',
        'password2': 'differentpassword',
    }
    response = client.post('/register/', data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'password2' in response.context['form'].errors
