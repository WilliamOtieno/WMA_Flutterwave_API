from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
