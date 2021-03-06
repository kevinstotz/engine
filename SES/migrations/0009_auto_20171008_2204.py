# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-09 02:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SES', '0008_auto_20171008_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Password',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Password', models.CharField(default=0, max_length=100)),
                ('Inserted', models.DateTimeField(auto_now_add=True, verbose_name='Time inserted')),
            ],
            options={
                'ordering': ('Id',),
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Role', models.CharField(max_length=50, verbose_name='Role of User')),
            ],
            options={
                'ordering': ('Id',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Username', models.CharField(max_length=50, verbose_name='User name')),
                ('Inserted', models.DateTimeField(auto_now_add=True, verbose_name='Time inserted')),
            ],
            options={
                'ordering': ('Id',),
            },
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Status', models.CharField(max_length=50, verbose_name='Status of User')),
            ],
            options={
                'ordering': ('Id',),
            },
        ),
        migrations.RenameField(
            model_name='emailtemplate',
            old_name='Body',
            new_name='Body_Text',
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='Filename',
            field=models.FileField(blank=True, null=True, upload_to='SES/static/templates/email/', verbose_name='Filename'),
        ),
        migrations.AddField(
            model_name='user',
            name='Status_Id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='SES.UserStatus'),
        ),
        migrations.AddField(
            model_name='password',
            name='User_Id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='SES.User'),
        ),
    ]
