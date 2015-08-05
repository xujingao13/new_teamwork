# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='last_steptime',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 12, 43, 17, 585279), blank=True),
        ),
    ]
