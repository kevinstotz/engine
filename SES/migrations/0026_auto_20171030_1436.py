# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SES', '0025_remove_passwordreset_password_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Login',
            new_name='UserLogin',
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_logged_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
