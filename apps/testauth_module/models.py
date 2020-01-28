from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class TestUser(AbstractUser):
    auth_id = models.IntegerField(null=True)
    subject = models.CharField(max_length=255, null=True)
    display_name = models.CharField(max_length=200)
    is_sync = models.BooleanField(default=False)
