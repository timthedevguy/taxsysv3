# Generated by Django 3.1.4 on 2020-12-15 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0014_auto_20201215_0657'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Settings',
            new_name='Setting',
        ),
    ]
