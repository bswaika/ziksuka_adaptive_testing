# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0007_auto_20170907_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='answered',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='learner',
            name='responses',
            field=models.TextField(blank=True, null=True),
        ),
    ]
