# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_auto_20150805_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='last_steptime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2015, 8, 5, 20, 45, 50, 458901)),
        ),
        migrations.AlterField(
            model_name='room',
            name='pausestart',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2015, 8, 5, 20, 45, 50, 458901)),
        ),
    ]
