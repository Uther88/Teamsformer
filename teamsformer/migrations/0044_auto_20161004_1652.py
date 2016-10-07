# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 16:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0043_auto_20160926_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 4, 16, 52, 58, 808593), verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='dialog',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 4, 16, 52, 58, 808593), verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(default=None, max_length=400, null=True, verbose_name='Text of message'),
        ),
        migrations.AlterField(
            model_name='team',
            name='needs',
            field=select_multiple_field.models.SelectMultipleField(blank=True, choices=[('developer', 'Developer'), ('investor', 'Investor'), ('sales_person', 'Salesperson')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('developer', 'Developer'), ('investor', 'Investor'), ('sales_person', 'Salesperson')], default=None, max_length=40, null=True, verbose_name='User role'),
        ),
    ]
