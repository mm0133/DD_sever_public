# Generated by Django 2.2.7 on 2020-07-28 06:56

import api.contests.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contestAnswer', models.FileField(blank=True, null=True, upload_to=api.contests.utils.comp_answer_upload_to)),
                ('deadline', models.DateTimeField()),
                ('timeline', models.TextField()),
                ('prize', models.IntegerField()),
                ('isForTraining', models.BooleanField(default=False)),
                ('winnerInterview', models.TextField(blank=True, null=True)),
                ('difficulty', models.CharField(choices=[('EASY', 'Easy'), ('NORMAL', 'Normal'), ('HARD', 'Hard')], default='Normal', max_length=6)),
                ('evliationMethod', models.CharField(choices=[('ACCURACY', 'Accuracy'), ('POPULARITY', 'Popularity')], default='Accuracy', max_length=10)),
                ('learningModel', models.CharField(max_length=255)),
                ('evaluationExplanation', models.TextField()),
                ('contestExplanation', models.TextField()),
                ('prizeExplanation', models.TextField()),
                ('dataExplanation', models.TextField()),
                ('profileThumb', models.ImageField(blank=True, null=True, upload_to='')),
                ('backThumb', models.ImageField(blank=True, null=True, upload_to='')),
                ('contestOverview', models.TextField(blank=True, null=True)),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContestUserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=api.contests.utils.user_answer_upload_to)),
                ('accuracy', models.FloatField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('constest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userAnswer', to='contests.Contest')),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContestFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('constest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contests.Contest')),
            ],
        ),
    ]
