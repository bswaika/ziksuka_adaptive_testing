# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0003_learner_answered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learner',
            name='answered',
        ),
        migrations.AlterField(
            model_name='learner',
            name='ability',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='difficulty',
            field=models.FloatField(),
        ),
    ]
