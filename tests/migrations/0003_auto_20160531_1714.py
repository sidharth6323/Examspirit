# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-31 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_auto_20160531_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='p_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='q_id',
            field=models.CharField(default=b'0770b940-2725-11e6-870e-6cc217e9b519', max_length=50),
        ),
    ]