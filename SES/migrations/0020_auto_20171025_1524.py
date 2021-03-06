# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 19:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SES', '0019_auto_20171025_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailaddress',
            name='User_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Login'),
        ),
        migrations.AlterField(
            model_name='login',
            name='User_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Login'),
        ),
        migrations.AlterField(
            model_name='name',
            name='User_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Login'),
        ),
        migrations.AlterField(
            model_name='passwordnotused',
            name='User_Id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='passwordreset',
            name='User_Id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
