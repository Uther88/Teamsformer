# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-12 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0024_auto_20160912_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, max_length=255, upload_to='users/avatars/'),
        ),
    ]
