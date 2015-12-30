# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0007_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chessplayer',
            name='last_ask',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 23, 10, 13, 19, 110893), blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='last_steptime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 23, 10, 13, 19, 109115), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='pausestart',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 23, 10, 13, 19, 109141), blank=True),
        ),
    ]
