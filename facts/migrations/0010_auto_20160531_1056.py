# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facts', '0009_auto_20160531_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='birth_day',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='birth_month',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='birth_year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='end_day',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='end_month',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='end_year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='start_day',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='start_month',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='start_year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
