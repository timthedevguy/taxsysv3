# Generated by Django 3.0.2 on 2020-01-27 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testauth_module', '0003_auto_20200126_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='testuser',
            name='display_name',
            field=models.CharField(default='None', max_length=200),
            preserve_default=False,
        ),
    ]
