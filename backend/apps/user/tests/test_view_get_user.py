import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


# API Client Fixture
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def active_user():
    return User.objects.create_user(
        email="test1@example.com",
        password="Testpassword1234!",
        fullname="Test User",
        phone_number="6282122223333",
        role="staff",
    )


# Test to Get User Personal Data
@pytest.mark.django_db
def test_functional_get_user_personal_data(api_client, active_user):
    """
    Test get user personal data
    Expected result:
    - User personal data
    """
    # arrange

    # act
    api_client.force_authenticate(user=active_user)
    response = api_client.get(reverse("user_retrieve"), {})

    # assert
    assert response.status_code == 200
    assert response.data["email"] == active_user.email
    assert response.data["fullname"] == active_user.fullname
    assert response.data["phone_number"] == active_user.phone_number
    assert response.data["role"] == active_user.role


# Test unauthorized get user personal data
@pytest.mark.django_db
def test_functional_unauthorized_get_user_personal_data(api_client):
    """
    Test unauthorized get user personal data
    Expected result:
    - Error because user is not authenticated
    """
    # arrange

    # act
    response = api_client.get(reverse("user_retrieve"), {})

    # assert
    assert response.status_code == 401
