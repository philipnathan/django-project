import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_password(password):

    if len(password) < 8:
        raise ValidationError(_("Password must be at least 8 characters long"))

    if not re.search(r"[A-Z]", password):
        raise ValidationError(_("Password must contain at least one uppercase letter"))

    if not re.search(r"[a-z]", password):
        raise ValidationError(_("Password must contain at least one lowercase letter"))

    if not re.search(r"[0-9]", password):
        raise ValidationError(_("Password must contain at least one number"))

    if not re.search(r"[!@#$%^&*]", password):
        raise ValidationError(
            _("Password must contain at least one special character (!@#$%^&*)")
        )


def validate_phone_number(phone_number):
    if len(phone_number) < 10:
        raise ValidationError(_("Phone number at least 10 digits long"))
    if not re.search(r"^62\d{9,11}$", phone_number):
        raise ValidationError(_("Phone number must start with 62"))
