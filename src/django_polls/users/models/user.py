from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UsernameValidator(ASCIIUsernameValidator):
    regex = r"^[\w.-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only English letters, "
        "numbers, and ./-/_ characters."
    )


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    username_validator = UsernameValidator

    class Meta(AbstractUser.Meta):
        abstract = False
        swappable = "AUTH_USER_MODEL"
        db_table = "auth_user"
