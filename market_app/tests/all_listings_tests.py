import pytest
from market_app.models import Listings


@pytest.mark.django_db
def test_all_listings_view_with_filters(authenticated_user1):
    response = authenticated_user1.get("/all_listings/")

    assert response.status_code == 200
    assert 'listings' in response.context
    assert 'page' in response.context
    assert 'listings_count' in response.context
    assert len(response.context['listings']) == 0
