import pytest
from django.urls import reverse


# Test create user
@pytest.mark.django_db
def test_functional_create_user(client):
    # arrange: Prepare user data
    user_data = {
        "email": "test1@example.com",
        "password": "Testpassword1234!",
        "password2": "Testpassword1234!",
        "fullname": "Test User",
        "phone_number": "6282122223333",
        "role": "staff",
    }

    # act: Call endpoint
    response = client.post(reverse("user_create"), user_data)
    print(response.data)
    print(response.status_code)

    # assert: Check response
    assert response.status_code == 201
    assert response.data["email"] == user_data["email"]
    assert response.data["role"] == user_data["role"]


# Test email normalization
@pytest.mark.django_db
@pytest.mark.parametrize(
    "email, expected_email",
    [
        # Test normal email
        ("test@example.com", "test@example.com"),
        # Test email with uppercase letters
        ("TEST@example.com", "test@example.com"),
        # Test email with mixed case letters
        ("TeSt@eXamPle.com", "test@example.com"),
        # Test email with blank spaces
        ("    test@example.com", "test@example.com"),
    ],
)
def test_functional_create_user_email_normalization(client, email, expected_email):
    """
    Test email normalization.
    Expected result:
    - Email is normalized to lowercase
    - Email is trimmed
    """

    # arrange
    user_data = {
        "email": email,
        "password": "Testpassword1234!",
        "password2": "Testpassword1234!",
        "fullname": "Test User",
        "phone_number": "6282122223333",
        "role": "staff",
    }

    # act
    response = client.post(reverse("user_create"), user_data)

    # assert
    assert response.status_code == 201
    assert response.data["email"] == expected_email


# Test password validation
@pytest.mark.django_db
@pytest.mark.parametrize(
    "password, expected_status_code",
    [
        # password less than 8 characters
        ("1234567", 400),
        # password without uppercase letter
        ("123456789", 400),
        # password without lowercase letter
        ("TEST1234", 400),
        # password without number
        ("TestPassword", 400),
        # password without special character
        ("TestPassword1234", 400),
        # password with all validations
        ("TestPassword1234!", 201),
    ],
)
def test_functional_create_user_password_validation(
    client, password, expected_status_code
):
    """
    Test password validation.
    Expected result:
    - Password must be at least 8 characters long
    - Password must contain at least one uppercase letter
    - Password must contain at least one lowercase letter
    - Password must contain at least one number
    - Password must contain at least one special character (!@#$%^&*)
    """
    # arrange
    user_data = {
        "email": "test@example.com",
        "password": password,
        "password2": password,
        "fullname": "Test User",
        "phone_number": "6282122223333",
        "role": "staff",
    }

    # act
    response = client.post(reverse("user_create"), user_data)

    # assert
    assert response.status_code == expected_status_code


# Test fullname validation
@pytest.mark.django_db
@pytest.mark.parametrize(
    "fullname, expected_status_code",
    [
        ("123", 400),
        ("1" * 129, 400),
        ("12345", 400),
        ("test!", 400),
        ("test1234", 400),
    ],
)
def test_functional_create_user_fullname_validation(
    client, fullname, expected_status_code
):
    """
    Test fullname validation.
    Expected result:
    - Fullname must be at least 4 characters long
    - Fullname must be at most 128 characters long
    - Fullname must be alphabetic
    - Fullname cannot contain special characters
    - Fullname cannot contain numbers
    """
    # arrange
    user_data = {
        "email": "test@example.com",
        "password": "Testpassword1234!",
        "password2": "Testpassword1234!",
        "fullname": fullname,
        "phone_number": "6282122223333",
        "role": "staff",
    }

    # act
    response = client.post(reverse("user_create"), user_data)

    # assert
    assert response.status_code == expected_status_code


# Test fullname normalization
@pytest.mark.django_db
@pytest.mark.parametrize(
    "fullname, expected_fullname",
    [
        # Test normal fullname
        ("test", "Test"),
        # Test fullname with uppercase letters
        ("TEST", "Test"),
        # Test fullname with mixed case letters
        ("TeSt", "Test"),
        # Test fullname with blank spaces
        ("    test", "Test"),
        ("test    ", "Test"),
        # Test fullname with consecutive spaces
        ("test   test", "Test Test"),
    ],
)
def test_functional_create_user_fullname_normalization(
    client, fullname, expected_fullname
):
    """
    Test fullname normalization.
    Expected result:
    - Fullname is trimmed
    - Fullname is capitalized
    - Fullname does not contain consecutive spaces
    """
    # arrange
    user_data = {
        "email": "test@example.com",
        "password": "Testpassword1234!",
        "password2": "Testpassword1234!",
        "fullname": fullname,
        "phone_number": "6282122223333",
        "role": "staff",
    }

    # act
    response = client.post(reverse("user_create"), user_data)

    # assert
    assert response.status_code == 201
    assert response.data["fullname"] == expected_fullname


# Test phone number validation
# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     "phone_number, expected_status_code",
#     [
#         # phone number must start with 62
#         ("12345678901", 400),
#         # phone number at least 11 digits long (including country code)
#         ("62821567890", 400),
#         # phone number at most 13 digits long (including country code)
#         ("628215678901234", 400)
#     ],
# )
