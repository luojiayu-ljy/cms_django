# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-22 03:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0002_remove_author_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='article',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='user',
        ),
        migrations.AddField(
            model_name='article',
            name='user_poll',
            field=models.ManyToManyField(blank=True, related_name='user_poll', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='user_keep',
            field=models.ManyToManyField(blank=True, related_name='user_keep', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Poll',
        ),
    ]
