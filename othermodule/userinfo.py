from player.models import *
from django.db.models import Q

def getNicknameByName(name):
	user = User.objects.get(username = name)
	nickname = ChessPlayer.objects.get(user = user).nick_name
	return nickname

def getIdByName(name):
	user = User.objects.get(username = name)
	return ChessPlayer.objects.get(user = user).id

def getNameById(id):
	return ChessPlayer.objects.get(id = id).user.username

def getRoomidByid(id):
	room = Room.objects.filter(Q(owner_id = id) | Q(guest_id = id))
	if room.count() == 0:
		return 0
	else:
		return room[0].id
