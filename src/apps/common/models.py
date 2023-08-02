import uuid

from model_utils.fields import UUIDField
from model_utils.models import TimeStampedModel

__all__ = [
    "BaseModel",
]


class BaseModel(TimeStampedModel):
    id = UUIDField(default=uuid.uuid4)

    class Meta:
        abstract = True
