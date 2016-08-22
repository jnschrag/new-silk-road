# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-22 20:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('facts', '0024_organization_mission_rendered'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='organization',
            managers=[
                ('publishable_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='financingorganizationdetails',
            name='members',
            field=models.ManyToManyField(related_name='financingorganization_memberships', to='facts.Organization'),
        ),
    ]
