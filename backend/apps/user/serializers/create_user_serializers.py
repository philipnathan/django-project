from ..validators import validate_password, validate_phone_number

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        label="Confirm Password",
    )

    phone_number = serializers.CharField(validators=[validate_phone_number])

    is_active = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "password2",
            "fullname",
            "phone_number",
            "role",
            "is_active",
        )

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": _("The two password fields didn't match.")}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        return get_user_model().objects.create_user(**validated_data)
