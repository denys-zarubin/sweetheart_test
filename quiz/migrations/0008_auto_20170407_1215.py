# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-07 12:15
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quiz', '0007_auto_20170407_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='questions',
        ),
        migrations.AddField(
            model_name='useranswer',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quiz.Question'),
            preserve_default=False,
        ),
    ]