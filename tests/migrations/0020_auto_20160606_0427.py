# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-05 22:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0019_auto_20160606_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='e_time',
            field=models.TimeField(default=datetime.datetime(2016, 6, 6, 4, 27, 3, 564000)),
        ),
    ]
