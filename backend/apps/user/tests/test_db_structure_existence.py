import pytest
from django.db import models

from apps.user.models import User


# check if table exists
def test_model_structure_table_exist():
    try:
        from apps.user.models import User  # noqa
    except ImportError:
        assert False, "User model cannot be imported"
    else:
        assert True, "User model was imported successfully"


# Check if all fields have the correct type
@pytest.mark.parametrize(
    "model, field_name, expected_type",
    [
        (User, "id", models.AutoField),
        (User, "email", models.EmailField),
        (User, "password", models.CharField),
        (User, "fullname", models.CharField),
        (User, "phone_number", models.CharField),
        (User, "role", models.CharField),
        (User, "is_staff", models.BooleanField),
        (User, "is_active", models.BooleanField),
        (User, "date_joined", models.DateTimeField),
        (User, "last_login", models.DateTimeField),
        (User, "groups", models.ManyToManyField),  # from PermissionsMixin
        (User, "user_permissions", models.ManyToManyField),  # from PermissionsMixin
        (User, "is_superuser", models.BooleanField),  # from PermissionsMixin
    ],
)
def test_model_structure_fields_exist(model, field_name, expected_type):
    assert hasattr(model, field_name), "Field '{}' not found in model '{}'".format(
        field_name, model.__name__
    )

    field = model._meta.get_field(field_name)

    assert isinstance(field, expected_type), "Field '{}' is not of type '{}'".format(
        field_name, expected_type
    )


# check if all fields are present (without extra or missing fields)
def test_model_structure_for_extra_or_missing_fields():
    expected_fields = set(
        [
            "id",
            "email",
            "password",
            "fullname",
            "phone_number",
            "role",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
            "groups",
            "user_permissions",
            "is_superuser",
        ]
    )

    model_fields = set(
        [field.name for field in User._meta.fields]
        + [field.name for field in User._meta.many_to_many]
    )

    errors = []

    if set(model_fields) != set(expected_fields):
        errors.append("Model fields are not correct")

    extra_fields = model_fields - expected_fields
    if extra_fields:
        errors.append("Model has extra fields: {}".format(extra_fields))

    missing_fields = expected_fields - model_fields
    if missing_fields:
        errors.append("Model is missing fields: {}".format(missing_fields))

    assert not errors, "\n".join(errors)


# validate relationship fields
