from django.db import models
from apps.testauth.models import TestUser
import uuid
import secrets

# Create your models here.
class Tenant(models.Model):
    name = models.CharField(null=False, max_length=255)
    identifier = models.CharField(null=False, max_length=255, default=uuid.uuid4)
    token = models.CharField(null=False, max_length=100,default=secrets.token_urlsafe)

    def corporations(self):
        return Corporation.objects.filter(tenant=self)

    def __str__(self):
        return self.name


class Corporation(models.Model):
    name = models.CharField(null=False, max_length=255)
    corporation_id = models.IntegerField(null=False)
    ceo_id = models.IntegerField(null=False)
    last_pull = models.DateField(null=True)
    processPayments = models.BooleanField(default=False)
    processTaxes = models.BooleanField(default=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Character(models.Model):
    character_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=255)
    corporation = models.ForeignKey(Corporation, on_delete=models.CASCADE)
    isValid = models.BooleanField(null=False, default=False)
    join_date = models.DateField(null=False)
    start_date = models.DateField(null=True)
    user = models.ForeignKey(TestUser, models.PROTECT)

    def __str__(self):
        return self.name


class Override(models.Model):
    tenantID = models.IntegerField(null=True)
    typeID = models.IntegerField(null=False)
    tax = models.FloatField(null=False)
    isOre = models.BooleanField(default=False)
