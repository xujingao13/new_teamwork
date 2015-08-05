# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChessPlayer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('image', models.ImageField(verbose_name='头像', upload_to='')),
                ('nick_name', models.CharField(verbose_name='游戏状态', max_length=256)),
                ('game_num', models.IntegerField(verbose_name='游戏次数', default=0)),
                ('game_grade', models.IntegerField(verbose_name='游戏积分', default=0)),
                ('game_state', models.CharField(verbose_name='游戏状态', max_length=128)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('publisher_id', models.IntegerField()),
                ('receiver_id', models.IntegerField()),
                ('type', models.CharField(verbose_name='信息类型', max_length=128)),
                ('content', models.CharField(verbose_name='信息内容', max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('user1_id', models.IntegerField()),
                ('user2_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('owner_id', models.IntegerField()),
                ('guest_id', models.IntegerField()),
                ('whose_turn', models.IntegerField()),
                ('game_state', models.CharField(verbose_name='游戏状态', max_length=128)),
                ('chess_board', models.CharField(verbose_name='棋盘状态', max_length=450)),
                ('last_chess_board', models.CharField(verbose_name='上一次棋盘状态', max_length=450)),
            ],
        ),
        migrations.CreateModel(
            name='WatchingGame',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('room_id', models.IntegerField()),
            ],
        ),
    ]
