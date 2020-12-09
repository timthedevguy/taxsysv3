# Generated by Django 3.1.4 on 2020-12-07 10:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0007_auto_20201207_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='token',
            field=models.CharField(default='EkMq9plbTTY', max_length=100),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='identifier',
            field=models.CharField(default=uuid.UUID('b59d003b-34d4-4f96-9017-a15bdc9d2e3d'), max_length=255),
        ),
    ]
