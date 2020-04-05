from django.db import models


# Create your models here.
class Override(models.Model):
    tenantID = models.IntegerField(null=True)
    typeID = models.IntegerField(null=False)
    tax = models.FloatField(null=False)
    isOre = models.BooleanField(default=False)
