# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-08 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SES', '0007_auto_20171008_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='Filename',
            field=models.FileField(blank=True, null=True, upload_to='static/templates/email/', verbose_name='Filename'),
        ),
    ]
