# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-31 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facts', '0030_auto_20161020_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=110, unique=True),
        ),
    ]
