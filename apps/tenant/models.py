from django.db import models


# Create your models here.
class Tenant(models.Model):
    name = models.CharField(null=False, max_length=255)
    identifier = models.CharField(null=False,max_length=255)

    def corporations(self):
        return Corporation.objects.filter(tenant=self)

    def __str__(self):
        return self.tenant_name


class Corporation(models.Model):
    name = models.CharField(null=False, max_length=255)
    corporation_id = models.IntegerField(null=False)
    ceo_id = models.IntegerField(null=False)
    ceo_name = models.CharField(null=False, max_length=255)
    last_pull = models.DateField(null=True)
    processPayments = models.BooleanField(default=False)
    processTaxes = models.BooleanField(default=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Override(models.Model):
    tenantID = models.IntegerField(null=True)
    typeID = models.IntegerField(null=False)
    tax = models.FloatField(null=False)
    isOre = models.BooleanField(default=False)
