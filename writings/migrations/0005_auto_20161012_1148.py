# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-12 15:48
from __future__ import unicode_literals

from django.db import migrations, models
import markymark.fields
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('writings', '0004_auto_20160808_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='subtitle',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=markymark.fields.MarkdownField(blank=True, help_text='Short text to be used where post might be promoted/referenced. Limited to 400 characters.', verbose_name='Summary/Description'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
