from django.db import models

# Create your models here.

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError(_("Email must be set"))

        email = self.normalize_email(email)
        email = email.strip().lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("staff", "staff"),
        ("supervisor", "supervisor"),
        ("manager", "manager"),
    )

    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(
        _("password"),
        max_length=128,
        null=False,
        blank=False,
    )
    fullname = models.CharField(_("fullname"), max_length=128, null=False, blank=False)
    phone_number = models.CharField(
        _("phone number"),
        max_length=14,
        null=False,
        blank=False,
        unique=True,
        validators=[
            MinLengthValidator(10),
            MaxLengthValidator(14),
            RegexValidator(
                regex=r"^62\d{9,11}$", message="Phone number must start with 62"
            ),
        ],
    )
    role = models.CharField(
        _("role"),
        max_length=20,
        null=False,
        blank=False,
        choices=ROLE_CHOICES,
        default="staff",
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="user_groups",
        blank=True,
        verbose_name="User Groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="user_permissions",
        blank=True,
        verbose_name="User Permissions",
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
