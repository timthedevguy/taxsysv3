from django.db import models


class CustomFloatField(models.Field):
    def db_type(self, connection):
        return 'float'


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


class TypeMaterials(models.Model):
    typeID = models.IntegerField(primary_key=True)
    materialTypeID = models.IntegerField(db_index=True)
    quantity = models.IntegerField(null=False)

    class Meta:
        db_table = 'invTypeMaterials'


class TypeAttributes(models.Model):
    typeID = models.IntegerField(primary_key=True)
    attributeID = models.IntegerField(null=False)
    valueInt = models.IntegerField(null=True)
    valueFloat = CustomFloatField(null=True)

    class Meta:
        db_table = 'dgmTypeAttributes'


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
