# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-06 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_auto_20160405_1609'),
        ('infrastructure', '0010_auto_20160330_1716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='initiative',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='project',
            name='geometries',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.GeometryCollection'),
        ),
    ]