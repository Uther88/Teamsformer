# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 12:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0009_auto_20160901_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_admin', to=settings.AUTH_USER_MODEL),
        ),
    ]
