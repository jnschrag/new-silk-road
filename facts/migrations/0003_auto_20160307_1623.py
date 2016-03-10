# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-07 21:23
from __future__ import unicode_literals

from django.db import migrations, models
import markymark.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0001_initial'),
        ('facts', '0002_auto_20160304_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='documents',
            field=models.ManyToManyField(blank=True, to='sources.Document'),
        ),
        migrations.AddField(
            model_name='event',
            name='notes',
            field=markymark.fields.MarkdownField(blank=True),
        ),
    ]