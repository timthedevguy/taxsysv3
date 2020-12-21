from django.db import models
from apps.eveonline_sde.utils import CustomFloatField


class TypeMaterials(models.Model):
    typeID = models.IntegerField(primary_key=True)
    materialTypeID = models.IntegerField(db_index=True)
    quantity = models.IntegerField(null=False)

    class Meta:
        db_table = 'invTypeMaterials'
