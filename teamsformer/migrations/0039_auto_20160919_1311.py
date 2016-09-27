# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsformer', '0038_message_recipient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dialog',
            options={'verbose_name': 'Dialog', 'verbose_name_plural': 'Dialogs'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created_date'], 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AlterField(
            model_name='dialog',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created data'),
        ),
    ]
