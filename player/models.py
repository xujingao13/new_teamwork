#coding:utf-8
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Room(models.Model):
    owner_id = models.IntegerField()
    guest_id = models.IntegerField()
    whose_turn = models.IntegerField()
    game_state = models.CharField(u'游戏状态',max_length=128)
    chess_board = models.CharField(u'棋盘状态',max_length=450)
    last_chess_board = models.CharField(u'上一次棋盘状态',max_length=450)


class Relationship(models.Model):
    user1_id = models.IntegerField()
    user2_id = models.IntegerField()


class WatchingGame(models.Model):
    user_id = models.IntegerField()
    room_id = models.IntegerField()


class Message(models.Model):
    publisher_id = models.IntegerField()
    receiver_id = models.IntegerField()
    type = models.CharField(u'信息类型',max_length=128)
    content = models.CharField(u'信息内容',max_length=400)


class ChessPlayer(models.Model):
    user = models.ForeignKey(User)
    image = models.ImageField(u'头像')
    nick_name = models.CharField(u'游戏状态',max_length=256)
    game_num = models.IntegerField(u'游戏次数',default=0)
    game_grade = models.IntegerField(u'游戏积分',default=0)
    game_state = models.CharField(u'游戏状态',max_length=128)

