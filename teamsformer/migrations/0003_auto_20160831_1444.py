# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0002_auto_20160831_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('DV', 'Developer'), ('IN', 'Investor'), ('SP', 'Sales person')], max_length=40, null=True, verbose_name='User role'),
        ),
    ]
