# Generated by Django 2.2.7 on 2020-08-10 10:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('educations', '0004_auto_20200810_1855'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LecuturePackage',
            new_name='LecturePackage',
        ),
    ]