# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-12 16:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('writings', '0005_auto_20161012_1148'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderedentry',
            unique_together=set([('entry', 'collection')]),
        ),
    ]
