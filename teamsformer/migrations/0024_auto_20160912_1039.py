# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-12 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0023_auto_20160912_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='noimage.png', max_length=255, upload_to='users/avatars/'),
        ),
    ]
