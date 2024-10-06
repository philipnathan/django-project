from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    new_password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}
    )
    new_email = serializers.EmailField(required=False)
    new_fullname = serializers.CharField(required=False)
    new_phone_number = serializers.CharField(required=False)

    class Meta:

        model = get_user_model()
        fields = (
            "new_email",
            "new_fullname",
            "new_phone_number",
            "new_password",
            "confirm_password",
            "current_password",
        )

    def validate(self, attrs):
        new_password = attrs.get("new_password", None)
        confirm_password = attrs.get("confirm_password", None)

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise serializers.ValidationError(
                    {"new_password": _("The two password fields didn't match.")}
                )
        return attrs

    def update(self, instance, validated_data):
        current_password = validated_data.pop("current_password", None)

        if not instance.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": _("Wrong password.")}
            )

        if validated_data.get("new_password"):
            instance.set_password(validated_data["new_password"])

        instance.email = validated_data.get("new_email", instance.email)
        instance.fullname = validated_data.get("new_fullname", instance.fullname)
        instance.phone_number = validated_data.get(
            "new_phone_number", instance.phone_number
        )

        instance.save()
        return instance
