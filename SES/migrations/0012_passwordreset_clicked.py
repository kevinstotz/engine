# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SES', '0011_auto_20171023_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordreset',
            name='Clicked',
            field=models.DateTimeField(auto_now=True, verbose_name='Time clicked'),
        ),
    ]
