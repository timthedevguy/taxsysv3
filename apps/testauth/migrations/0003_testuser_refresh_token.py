# Generated by Django 3.0.3 on 2020-02-04 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testauth', '0002_testuser_last_alt_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='testuser',
            name='refresh_token',
            field=models.TextField(null=True),
        ),
    ]
