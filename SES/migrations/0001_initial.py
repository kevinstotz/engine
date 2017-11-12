# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-07 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Email', models.EmailField(default='noemail@noemail.com', max_length=100, verbose_name='Email of Register')),
                ('First_Name', models.CharField(max_length=50, verbose_name='First Name of Register')),
                ('Last_Name', models.CharField(max_length=50, verbose_name='Last Name of Register')),
                ('IP_Address', models.CharField(blank=True, max_length=50, verbose_name='IP Address of Register')),
                ('User_Agent', models.CharField(blank=True, max_length=255, verbose_name='User Agent of Register')),
                ('Authorization_Code', models.CharField(max_length=255, verbose_name='Auto Generated Auth Code')),
                ('Inserted', models.DateTimeField(auto_now_add=True, verbose_name='Time inserted')),
            ],
            options={
                'ordering': ('Id',),
            },
        ),
    ]
