# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facts', '0016_remove_companydetails_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='staff_size',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Staff/Personnel count'),
        ),
    ]
