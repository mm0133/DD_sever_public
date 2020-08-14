# Generated by Django 2.2.7 on 2020-08-14 08:43

import api.contests.utils
from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_auto_20200814_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customprofile',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='user_1/profile', null=True, upload_to=api.contests.utils.user_profile_image_path),
        ),
        migrations.AlterField(
            model_name='customprofile',
            name='smallImage',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='user_1/profile', null=True, upload_to=api.contests.utils.user_profile_image_path),
        ),
        migrations.AlterField(
            model_name='team',
            name='smallImage',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='user_1/profile', null=True, upload_to=api.contests.utils.team_profile_image_path),
        ),
    ]
