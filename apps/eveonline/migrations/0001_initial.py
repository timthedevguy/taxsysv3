# Generated by Django 3.0.3 on 2020-03-15 17:27

import apps.eveonline.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('typeID', models.IntegerField(primary_key=True, serialize=False)),
                ('groupID', models.IntegerField(db_index=True, null=True)),
                ('typeName', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True)),
                ('mass', models.FloatField(null=True)),
                ('volume', models.FloatField(null=True)),
                ('capacity', models.FloatField(null=True)),
                ('portionSize', models.IntegerField(null=True)),
                ('raceID', models.IntegerField(null=True)),
                ('basePrice', models.DecimalField(decimal_places=4, max_digits=19)),
                ('published', models.BooleanField(null=True)),
                ('marketGroupID', models.IntegerField(null=True)),
                ('iconID', models.IntegerField(null=True)),
                ('soundID', models.IntegerField(null=True)),
                ('graphicID', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'invTypes',
            },
        ),
        migrations.CreateModel(
            name='TypeAttributes',
            fields=[
                ('typeID', models.IntegerField(primary_key=True, serialize=False)),
                ('attributeID', models.IntegerField()),
                ('valueInt', models.IntegerField(null=True)),
                ('valueFloat', apps.eveonline.models.CustomFloatField(null=True)),
            ],
            options={
                'db_table': 'dgmTypeAttributes',
            },
        ),
        migrations.CreateModel(
            name='TypeMaterials',
            fields=[
                ('typeID', models.IntegerField(primary_key=True, serialize=False)),
                ('materialTypeID', models.IntegerField(db_index=True)),
                ('quantity', models.IntegerField()),
            ],
            options={
                'db_table': 'invTypeMaterials',
            },
        ),
    ]
