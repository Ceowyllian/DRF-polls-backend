from typing import TypeVar

from django.contrib.auth.models import AbstractUser
from django.db import models

ModelType = TypeVar('ModelType', bound=models.Model)
UserModelType = TypeVar('UserModelType', bound=AbstractUser)
