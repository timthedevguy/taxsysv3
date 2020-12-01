from django.db import models


# Create your models here.
class Tenant(models.Model):
    tenant_name = models.CharField(null=False, max_length=255)
    ceo_subject = models.CharField(null=False, max_length=255)
    corporation_id = models.IntegerField(null=False)


class Override(models.Model):
    tenantID = models.IntegerField(null=True)
    typeID = models.IntegerField(null=False)
    tax = models.FloatField(null=False)
    isOre = models.BooleanField(default=False)
