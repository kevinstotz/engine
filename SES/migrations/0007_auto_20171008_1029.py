# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-08 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SES', '0006_auto_20171008_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='Filename',
            field=models.FileField(blank=True, null=True, upload_to='templates/email', verbose_name='Filename'),
        ),
        migrations.AlterField(
            model_name='register',
            name='Authorization_Code',
            field=models.CharField(max_length=20, verbose_name='Auto Generated Auth Code'),
        ),
    ]
