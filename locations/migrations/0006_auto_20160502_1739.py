# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 21:39
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_geometrystore_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='multigeometry',
            options={},
        ),
        migrations.AlterField(
            model_name='geometrystore',
            name='centroid',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, editable=False, null=True, srid=4326),
        ),
    ]