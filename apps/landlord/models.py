from django.db import models


# Create your models here.
class Setting(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    tenant = models.CharField(max_length=10)
