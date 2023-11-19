from django.contrib.auth import get_user_model
from django.db import models

from db.common.models import BaseModel, WithOwnerMixin
from db.common.types import UserModelType

User: UserModelType = get_user_model()


class Question(
    WithOwnerMixin,
    BaseModel,
):
    title = models.TextField(
        null=False,
        blank=False,
    )
    text = models.TextField(
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.title
