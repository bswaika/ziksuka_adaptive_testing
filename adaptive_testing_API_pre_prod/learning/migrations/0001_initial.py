# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('choices', models.TextField()),
                ('answer', models.CharField(max_length=2)),
                ('difficulty', models.DecimalField(decimal_places=5, max_digits=6)),
            ],
        ),
    ]