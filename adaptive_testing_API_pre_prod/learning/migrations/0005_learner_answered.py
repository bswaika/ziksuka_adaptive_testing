# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0004_auto_20170906_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='answered',
            field=models.TextField(null=True),
        ),
    ]