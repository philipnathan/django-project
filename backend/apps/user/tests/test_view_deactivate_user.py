import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def active_user():
    return User.objects.create_user(
        email="test1@example.com",
        password="Testpassword1234!",
        fullname="Test User",
        phone_number="6282122223333",
        role="staff",
    )


@pytest.fixture
def inactive_user():
    return User.objects.create_user(
        email="test2@example.com",
        password="Testpassword1234!",
        fullname="Test User",
        phone_number="6282122223333",
        role="staff",
        is_active=False,
    )


@pytest.fixture
def superuser():
    return User.objects.create_superuser(
        email="test3@example.com",
        password="Testpassword1234!",
        fullname="Test User",
        phone_number="6282122223333",
    )


@pytest.fixture
def staff_user():
    return User.objects.create_user(
        email="test4@example.com",
        password="Testpassword1234!",
        fullname="Test User",
        phone_number="6282122223333",
        role="staff",
        is_staff=True,
    )


# API Client Fixture
@pytest.fixture
def api_client():
    return APIClient()


# Test deactivate user
@pytest.mark.django_db
def test_functional_deactivate_user(api_client, active_user):
    """
    Test deactivate user
    Expected result:
    - User is deactivated
    """
    # arrange
    api_client.force_authenticate(user=active_user)

    # act
    response = api_client.put(reverse("user_deactivate"), {})

    # assert
    assert response.status_code == 200

    active_user.refresh_from_db()
    assert active_user.is_active is False


# Test deactivate inactive user
@pytest.mark.django_db
def test_functional_deactivate_inactive_user(api_client, inactive_user):
    """
    Test deactivate inactive user
    Expected result:
    - Error because user is already inactive
    """
    # arrange
    api_client.force_authenticate(user=inactive_user)

    # act
    response = api_client.put(reverse("user_deactivate"), {})

    # assert
    assert response.status_code == 400


# Test deactivate superuser
@pytest.mark.django_db
def test_functional_deactivate_superuser(api_client, superuser):
    """
    Test deactivate superuser
    Expected result:
    - Error because cannot deactivate superuser
    """
    # arrange
    api_client.force_authenticate(user=superuser)

    # act
    response = api_client.put(reverse("user_deactivate"), {})

    # assert
    assert response.status_code == 400


# Test deactivate staff user
@pytest.mark.django_db
def test_functional_deactivate_staff_user(api_client, staff_user):
    """
    Test deactivate staff user
    Expected result:
    - Error because cannot deactivate staff user
    """
    # arrange
    api_client.force_authenticate(user=staff_user)

    # act
    response = api_client.put(reverse("user_deactivate"), {})

    # assert
    assert response.status_code == 400


# Test attempt re-activate deactivated user
@pytest.mark.django_db
def test_functional_attempt_reactivate_deactivated_user(api_client, inactive_user):
    """
    Test attempt re-activate deactivated user
    Expected result:
    - Error because this API endpoint is only for deactivated users
    """
    # arrange
    api_client.force_authenticate(user=inactive_user)

    # act
    response = api_client.put(reverse("user_deactivate"), {"is_active": True})

    # assert
    assert response.status_code == 400


# Test unauthorized access
@pytest.mark.django_db
def test_functional_unauthorized_access(api_client):
    """
    Test unauthorized access
    Expected result:
    - Error because user is not authenticated
    """
    # arrange
    # act
    response = api_client.put(reverse("user_deactivate"), {})

    # assert
    assert response.status_code == 401
