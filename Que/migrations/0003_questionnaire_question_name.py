# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-30 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Que', '0002_auto_20180130_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='question_name',
            field=models.CharField(max_length=200, null=True, verbose_name='问卷名称'),
        ),
    ]
