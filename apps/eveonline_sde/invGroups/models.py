from django.db import models


class Groups(models.Model):
    groupID = models.IntegerField(primary_key=True)
    categoryID = models.IntegerField(db_index=True)
    groupName = models.CharField(null=True, max_length=100)
    iconID = models.IntegerField(null=True)
    useBasePrice = models.BooleanField(null=True)
    anchored = models.BooleanField(null=True)
    anchorable = models.BooleanField(null=True)
    fittableNonSingleton = models.BooleanField(null=True)
    published = models.BooleanField(null=True)

    class Meta:
        db_table = 'invGroups'
