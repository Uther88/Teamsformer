# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 11:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0046_auto_20161010_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 10, 11, 18, 19, 799804), verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='dialog',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 10, 11, 18, 19, 799804), verbose_name='Updated date'),
        ),
    ]
