# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='last_steptime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2015, 8, 5, 20, 45, 24, 773323)),
        ),
        migrations.AlterField(
            model_name='room',
            name='pausestart',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2015, 8, 5, 20, 45, 24, 773323)),
        ),
    ]
