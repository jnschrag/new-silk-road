# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-14 18:38
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('facts', '0028_populate_organization_uuid_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='identifier',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
