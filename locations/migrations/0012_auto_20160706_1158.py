# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 15:58
from __future__ import unicode_literals

from django.db import migrations
from django.utils.text import slugify


def add_country_slugs(apps, schema_editor):
    Country = apps.get_model('locations', 'Country')
    db_alias = schema_editor.connection.alias
    for country in Country.objects.using(db_alias).all():
        country.slug = slugify(country.name, allow_unicode=True)
        country.save()


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0011_country_slug'),
    ]

    operations = [
        migrations.RunPython(add_country_slugs)
    ]
