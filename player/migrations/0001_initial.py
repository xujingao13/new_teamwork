# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChessPlayer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='头像')),
                ('nick_name', models.CharField(max_length=256, verbose_name='游戏状态')),
                ('game_num', models.IntegerField(verbose_name='游戏次数', default=0)),
                ('game_grade', models.IntegerField(verbose_name='游戏积分', default=0)),
                ('game_state', models.CharField(max_length=128, verbose_name='游戏状态')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('publisher_id', models.IntegerField()),
                ('receiver_id', models.IntegerField()),
                ('type', models.CharField(max_length=128, verbose_name='信息类型')),
                ('content', models.CharField(max_length=400, verbose_name='信息内容')),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('user1_id', models.IntegerField()),
                ('user2_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('owner_id', models.IntegerField()),
                ('guest_id', models.IntegerField()),
                ('whose_turn', models.IntegerField()),
                ('game_state', models.CharField(max_length=128, verbose_name='游戏状态')),
                ('chess_board', models.CharField(max_length=450, verbose_name='棋盘状态')),
                ('last_chess_board', models.CharField(max_length=450, verbose_name='上一次棋盘状态')),
                ('last_steptime', models.DateTimeField(blank=True, default=datetime.datetime(2015, 8, 5, 20, 42, 37, 294029))),
                ('pausestart', models.DateTimeField(blank=True, default=datetime.datetime(2015, 8, 5, 20, 42, 37, 294029))),
            ],
        ),
        migrations.CreateModel(
            name='WatchingGame',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('room_id', models.IntegerField()),
            ],
        ),
    ]
