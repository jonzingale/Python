# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-06-04 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('color_summary', '0002_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='json',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
