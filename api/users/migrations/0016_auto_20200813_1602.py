# Generated by Django 2.2.7 on 2020-08-13 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20200813_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customprofile',
            name='nickname',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customprofile',
            name='phoneNumber',
            field=models.CharField(max_length=11),
        ),
    ]