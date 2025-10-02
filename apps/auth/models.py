from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    class Meta:
        db_table = "auth_user"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.get_full_name() or self.username
