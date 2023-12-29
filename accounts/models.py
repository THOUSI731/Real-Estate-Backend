from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=15,null=True)
    is_tenant = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.email