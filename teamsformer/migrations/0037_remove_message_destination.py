# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 18:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0036_auto_20160917_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='destination',
        ),
    ]
