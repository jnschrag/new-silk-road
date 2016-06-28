# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-13 18:08
from __future__ import unicode_literals

from django.db import migrations


def forward_func(apps, schema_editor):
    CompanyDetails = apps.get_model("facts", "CompanyDetails")
    db_alias = schema_editor.connection.alias
    for obj in CompanyDetails.objects.using(db_alias).filter(sector__isnull=False):
        obj.sectors = [obj.sector]
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('facts', '0014_companydetails_sectors'),
    ]

    operations = [
        migrations.RunPython(forward_func, migrations.RunPython.noop)
    ]