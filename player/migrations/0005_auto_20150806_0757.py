# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0004_auto_20150805_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='chessplayer',
            name='last_ask',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 6, 7, 57, 1, 925316), blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='last_steptime',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 6, 7, 57, 1, 923725), blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='pausestart',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 6, 7, 57, 1, 923749), blank=True),
        ),
    ]
