# Generated by Django 3.1 on 2020-12-03 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0003_auto_20201203_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporation',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='override',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]