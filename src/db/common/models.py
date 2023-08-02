import uuid

from django.contrib.auth import get_user_model
from django.db import models
from model_utils.fields import UUIDField
from model_utils.models import TimeStampedModel

__all__ = [
    "BaseModel",
    "WithOwnerMixin",
]

User = get_user_model()


class BaseModel(TimeStampedModel):
    id = UUIDField(default=uuid.uuid4)

    class Meta:
        abstract = True


class WithOwnerMixin(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=False,
        help_text="Owner",
    )

    class Meta:
        abstract = True
