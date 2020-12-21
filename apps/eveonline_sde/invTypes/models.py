from django.db import models
from apps.eveonline_sde.utils import CustomFloatField


class Type(models.Model):
    typeID = models.IntegerField(primary_key=True)
    groupID = models.IntegerField(null=True, db_index=True)
    typeName = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    mass = models.FloatField(null=True)
    volume = models.FloatField(null=True)
    capacity = models.FloatField(null=True)
    portionSize = models.IntegerField(null=True)
    raceID = models.IntegerField(null=True)
    basePrice = models.DecimalField(max_digits=19, decimal_places=4)
    published = models.BooleanField(null=True)
    marketGroupID = models.IntegerField(null=True)
    iconID = models.IntegerField(null=True)
    soundID = models.IntegerField(null=True)
    graphicID = models.IntegerField(null=True)

    class Meta:
        db_table = 'invTypes'
