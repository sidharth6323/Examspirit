# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-01 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0013_auto_20160602_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='instructions',
            field=models.TextField(max_length=10000),
        ),
    ]
