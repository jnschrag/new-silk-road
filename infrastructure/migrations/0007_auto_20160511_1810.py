# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-11 22:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0006_remove_uuid_null'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectfunding',
            options={'ordering': ['project__name', 'created_at'], 'verbose_name_plural': 'project funders'},
        ),
    ]
