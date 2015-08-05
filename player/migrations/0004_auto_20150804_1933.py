# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_auto_20150804_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='pausestart',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2015, 8, 4, 19, 33, 27, 958246)),
        ),
        migrations.AlterField(
            model_name='room',
            name='last_steptime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2015, 8, 4, 19, 33, 27, 958225)),
        ),
    ]
