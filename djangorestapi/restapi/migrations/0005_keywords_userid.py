# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 12:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restapi', '0004_auto_20170728_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywords',
            name='UserID',
            field=models.ForeignKey(blank=True, db_column='username', default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]