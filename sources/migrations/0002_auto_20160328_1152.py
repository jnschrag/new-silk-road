# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='url',
            field=models.URLField(blank=True, max_length=500, verbose_name='URL'),
        ),
    ]
