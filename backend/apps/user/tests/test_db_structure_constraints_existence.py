# validate field constraints

import pytest

from apps.user.models import User


# validate nullable and blank fields
@pytest.mark.parametrize(
    "model, field_name, allow_null, allow_blank",
    [
        (User, "email", False, False),
        (User, "password", False, False),
        (User, "fullname", False, False),
        (User, "phone_number", False, False),
        (User, "role", False, False),
    ],
)
def test_model_null_and_blank_constraints(model, field_name, allow_null, allow_blank):

    field = model._meta.get_field(field_name)

    assert field.null == allow_null
    assert field.blank == allow_blank


# validate unique fields
@pytest.mark.parametrize(
    "model, field_name, is_unique",
    [
        (User, "email", True),
        (User, "fullname", False),
        (User, "phone_number", True),
        (User, "role", False),
    ],
)
def test_model_unique_constraints(model, field_name, is_unique):

    field = model._meta.get_field(field_name)

    assert field.unique == is_unique


# validate max_length fields
@pytest.mark.parametrize(
    "model, field_name, expected_max_length",
    [
        (User, "email", 254),
        (User, "fullname", 128),
        (User, "phone_number", 14),
        (User, "role", 20),
    ],
)
def test_model_max_length_constraints(model, field_name, expected_max_length):

    field = model._meta.get_field(field_name)

    assert field.max_length == expected_max_length


# validate default values
@pytest.mark.parametrize(
    "model, field_name, expected_default",
    [
        (User, "role", "staff"),
        (User, "is_staff", False),
        (User, "is_active", True),
    ],
)
def test_model_default_constraints(model, field_name, expected_default):

    field = model._meta.get_field(field_name)

    assert field.default == expected_default
