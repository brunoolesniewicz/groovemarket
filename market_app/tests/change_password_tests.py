import pytest
from market_app.forms import PasswordChangeForm


@pytest.mark.django_db
def test_change_password_view_get(authenticated_user1):
    response = authenticated_user1.get('/my_account/password/')

    assert response.status_code == 200
    assert isinstance(response.context['form'], PasswordChangeForm)


@pytest.mark.django_db
def test_change_password_view_post(authenticated_user1, user1):
    new_password = 'newpassword123'

    response = authenticated_user1.post('/my_account/password/', {
        'old_password': 'testpassword1',
        'new_password1': new_password,
        'new_password2': new_password,
    })

    assert response.status_code == 302
    user1.refresh_from_db()
    assert user1.check_password(new_password)


@pytest.mark.django_db
def test_change_password_view_post(authenticated_user1, user1):
    new_password = 'newpassword123'

    response = authenticated_user1.post('/my_account/password/', {
        'old_password': 'testpassword1',
        'new_password1': new_password,
        'new_password2': 'differentpassword',
    })

    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], PasswordChangeForm)
    assert 'Nowe hasła nie są takie same.' in response.context['form'].errors['new_password2']
