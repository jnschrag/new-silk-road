# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0006_project_extra_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectfunding',
            name='amount',
            field=models.BigIntegerField(blank=True, help_text='Values in whole units (dollars, etc.)', null=True),
        ),
    ]