import pytest

# from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


# API Client Fixture
@pytest.fixture
def api_client():
    return APIClient()


# User Fixture
@pytest.fixture
def active_user():
    return User.objects.create_user(
        email="test1@example.com",
        password="Testpassword1234!",
        fullname="Test User",
        phone_number="6282122223333",
        role="staff",
    )


# # Test update for every property
# @pytest.mark.django_db
# @pytest.mark.parametrize("property, value, expected_value", [])
# def test_functional_update_user_property_except_password(
#     property, value, expected_value, api_client, active_user
# ):
#     # arrange
#     change_data = {property: value, "current_password": active_user.password}

#     api_client.force_authenticate(user=active_user)

#     # act
#     response = api_client.put(reverse("user_update"), change_data)

#     # assert
#     assert response.status_code == 200
