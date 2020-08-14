# Generated by Django 2.2.7 on 2020-08-13 10:17

import imagekit.models.fields
from django.db import migrations

import api.contests.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20200813_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customprofile',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='user_5/profile', null=True, upload_to=api.contests.utils.user_profile_image_path),
        ),
        migrations.AlterField(
            model_name='customprofile',
            name='smallImage',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='user_5/profile', null=True, upload_to=api.contests.utils.user_profile_image_path),
        ),
    ]