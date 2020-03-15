from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime
from django.conf import settings


# Create your models here.
class TestUser(AbstractUser):
    auth_id = models.IntegerField(null=True)
    subject = models.CharField(max_length=255, null=True)
    display_name = models.CharField(max_length=200)
    is_sync = models.BooleanField(default=False)
    last_alt_check = models.DateField(null=True)
    refresh_token = models.TextField(null=True)

    def is_stale(self):
        if self.last_alt_check is None:
            return True
        elif datetime.now() > (self.last_alt_check + timedelta(settings.FORCE_ALT_REFRESH_INTERVAL)):
            return True
        return False
