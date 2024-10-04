# validate field constraints

import pytest
from django.db import models

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
