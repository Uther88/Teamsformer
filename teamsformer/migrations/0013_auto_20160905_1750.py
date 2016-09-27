# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 14:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0012_user_contact_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact_list',
            field=models.ManyToManyField(blank=True, related_name='_user_contact_list_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
