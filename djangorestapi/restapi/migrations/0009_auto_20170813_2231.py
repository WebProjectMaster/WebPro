# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0008_auto_20170812_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='Hash_url',
            field=models.URLField(max_length=254, verbose_name='hash_url'),
        ),
        migrations.AlterField(
            model_name='pages',
            name='Url',
            field=models.URLField(max_length=256, verbose_name='url'),
        ),
    ]