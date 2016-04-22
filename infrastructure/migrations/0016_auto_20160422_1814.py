# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0015_auto_20160422_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Project name/title'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=310),
        ),
    ]
