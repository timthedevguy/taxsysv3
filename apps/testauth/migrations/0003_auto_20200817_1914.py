# Generated by Django 3.1 on 2020-08-17 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testauth', '0002_testuser_last_alt_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]