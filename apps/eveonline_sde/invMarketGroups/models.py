from django.db import models


class MarketGroups(models.Model):
    marketGroupID = models.IntegerField(primary_key=True)
    parentGroupID = models.IntegerField(null=True)
    marketGroupName = models.CharField(null=True, max_length=100)
    description = models.CharField(max_length=3000, null=True)
    iconID = models.IntegerField(null=True)
    hasTypes = models.BooleanField(null=True)

    class Meta:
        db_table = 'invMarketGroups'
