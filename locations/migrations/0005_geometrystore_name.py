# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_geometrystore_centroid'),
    ]

    operations = [
        migrations.AddField(
            model_name='geometrystore',
            name='label',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
