# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 13:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0031_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='destination',
            field=models.ForeignKey(max_length=40, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recived_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
