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
    if len(phone_number) < 11:
        raise ValidationError(_("Phone number at least 11 digits long"))
    if len(phone_number) > 13:
        raise ValidationError(_("Phone number at most 13 digits long"))
    if not re.search(r"^62\d{9,11}$", phone_number):
        raise ValidationError(_("Phone number must start with 62"))


def validate_fullname(fullname):
    if len(fullname) < 4:
        raise ValidationError(_("Fullname must be at least 4 characters long"))
    if len(fullname) > 128:
        raise ValidationError(_("Fullname must be at most 128 characters long"))

    # check if fullname only contains alphabetic characters
    if not re.match(r"^[a-zA-Z\s]+$", fullname):
        raise ValidationError(
            _(
                "Fullname must be alphabetic and cannot contain special characters or numbers."
            )
        )
