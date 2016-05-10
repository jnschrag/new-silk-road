# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 20:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0002_auto_20160502_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectfunding',
            options={'ordering': ['project__name'], 'verbose_name_plural': 'project funders'},
        ),
        migrations.AddField(
            model_name='projectfunding',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime.now(tz=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectfunding',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime.now(tz=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectfunding',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funding', to='infrastructure.Project'),
        ),
    ]
