# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-07 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SES', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='IP_Address',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='IP Address of Register'),
        ),
    ]
