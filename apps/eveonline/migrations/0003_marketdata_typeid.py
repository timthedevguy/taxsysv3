# Generated by Django 3.0.4 on 2020-04-05 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eveonline', '0002_marketdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketdata',
            name='typeID',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]