# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 20:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SES', '0022_auto_20171025_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passwordnotused',
            name='Status_Id',
        ),
        migrations.RemoveField(
            model_name='passwordnotused',
            name='User_Id',
        ),
        migrations.DeleteModel(
            name='PasswordNotUsed',
        ),
    ]
