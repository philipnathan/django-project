from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserDeactivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("is_active",)

    def validate_is_active(self, value):
        if value:
            raise serializers.ValidationError(
                {"is_active": _("Please set to false to deactivate user")}
            )

        if self.instance.is_active is False:
            raise serializers.ValidationError(
                {"is_active": _("User is already deactivated")}
            )

        if self.instance.is_staff or self.instance.is_superuser:
            raise serializers.ValidationError(
                {"is_active": _("Cannot deactivate staff or superuser")}
            )

        return value
