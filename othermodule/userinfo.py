from player.models import ChessPlayer

def getNicknameByName(name):
	user = User.objects.get(username = name).user
	nickname = ChessPlayer.objects.get(user = user)
	return nickname

def getIdByName(name):
	return User.objects.get(username = name).id

def getNameById(id):
	return ChessPlayer.objects.get(id = id).username
