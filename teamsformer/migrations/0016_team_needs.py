# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-08 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0015_auto_20160908_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='needs',
            field=models.CharField(blank=True, choices=[('DV', 'Developer'), ('IN', 'Investor'), ('SP', 'Sales person')], max_length=100, null=True, verbose_name='Vacant places'),
        ),
    ]
