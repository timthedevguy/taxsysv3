from django.db import models


# Create your models here.
class MarketData(models.Model):
    weightedAverage = models.DecimalField(max_digits=19, decimal_places=2, null=False)
    max = models.DecimalField(max_digits=19, decimal_places=2, null=False)
    min = models.DecimalField(max_digits=19, decimal_places=2, null=False)
    stddev = models.DecimalField(max_digits=19, decimal_places=2, null=False)
    median = models.DecimalField(max_digits=19, decimal_places=2, null=False)
    volume = models.BigIntegerField(null=False)
    orderCount = models.BigIntegerField(null=False)
    percentile = models.DecimalField(max_digits=19, decimal_places=2, null=False)
    date = models.DateField(null=False)
    typeID = models.IntegerField(null=False)
