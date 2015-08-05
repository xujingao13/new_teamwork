# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_auto_20150805_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='last_steptime',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 5, 20, 46, 50, 326282), blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='pausestart',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 5, 20, 46, 50, 326282), blank=True),
        ),
    ]
