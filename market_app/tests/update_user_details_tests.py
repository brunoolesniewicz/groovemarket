import pytest
from market_app.forms import UpdateUserDetailsForm


@pytest.mark.django_db
def test_update_user_details_view_get(authenticated_user1):
    response = authenticated_user1.get('/my_account/edit/')

    assert response.status_code == 200
    assert isinstance(response.context['form'], UpdateUserDetailsForm)


@pytest.mark.django_db
def test_update_user_details_view_post(authenticated_user1, user1):
    assert user1.first_name == 'Test1'
    response = authenticated_user1.post('/my_account/edit/', {
        'first_name': 'NewFirstName'
    })

    assert response.status_code == 302
    user1.refresh_from_db()
    assert user1.first_name == 'NewFirstName'
