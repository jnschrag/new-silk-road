# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-22 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20160822_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionitem',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
