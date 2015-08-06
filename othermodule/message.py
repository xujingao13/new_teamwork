from player.models import *
from othermodule.game import *
from othermodule.userinfo import *
from datetime import datetime

def m_oneStep(message):
	x, y, id_self, id_enemy, id_room = [eval(i) for i in message.split('_')]
	currentroom = Room.objects.get(id = id_room)
	currentroom.whose_turn = id_enemy
	currentroom.last_steptime = datetime.now()
	chessboard = currentroom.chess_board
	currentroom.last_chess_board = chessboard
	index = x + y * 15
	if id_self == currentroom.owner_id:
		color = '1'
	else:
		color = '2'
	newChessboard = chessboard[:index] + color + chessboard[index + 1:]
	currentroom.chess_board = newChessboard
	message_content = 'ONESTEP' + '&' + str(x) + '_' + str(y)
	print(message_content)
	m = Message(publisher_id = 0, receiver_id = id_enemy, type = 'ONESTEP', content = message_content)
	m.save()
	print('m_oneStep flag1')
	if g_ifGameOver(newChessboard, x, y, color):
		print('m_oneStep flag2')
		currentroom.game_state = 'pre_game'
		g_EndGame(ifTie = False, winner = id_self, loser = id_enemy, room = id_room)
	currentroom.save()
	print('m_oneStep over')

def m_rGameStart(message):
	id_self, id_enemy, id_room = [eval(i) for i in message.split('_')]
	message_content = 'RGAMESTART'
	print(message_content)
	m = Message(publisher_id = 0, receiver_id = id_enemy, type = 'RGAMESTART', content = message_content)
	m.save()

def m_aGameStart(message):
	id_self, id_enemy, id_room = [eval(i) for i in message.split('_')]
	message_content = 'GAMESTART'
	m = Message(publisher_id = 0, receiver_id = id_self, type = 'GAMESTART', content = message_content)
	m.save()
	m = Message(publisher_id = 0, receiver_id = id_enemy, type = 'GAMESTART', content = message_content)
	m.save()
	self = ChessPlayer.objects.get(id = id_self)
	enemy = ChessPlayer.objects.get(id = id_enemy)
	self.game_state = 'gaming'
	enemy.game_state = 'gaming'
	g_gameStart(id_room)

def m_naGameStart(message):
	id_enemy = eval(message)
	message_content = 'NAGAMESTART'
	m = Message(publisher_id = 0, receiver_id = id_enemy, type = 'NAGAMESTART', content = message_content)
	m.save()

def m_rFriend(message):
	id_sender, name_receiver = message.split('_')
	id_sender = eval(id_sender)
	id_receiver = getIdByName(name_receiver)
	name_sender = getNameById(id_sender)
	nickname_sender = getNicknameByName(name_sender)
	message_content = 'RFRIEND' + '&' + str(id_sender) + '_' + name_sender + '_' + nickname_sender
	m = Message(publisher_id = 0, receiver_id = id_receiver, type = 'RFRIEND', content = message_content)
	m.save()

def m_aFriend(message):
	id_receiver, name_sender = message.split('_')
	id_sender = getIdByName(name_sender)
	name_receiver = getNameById(id_receiver)
	r = Relationship(user1_id = id_receiver, user2_id = id_sender)
	r.save()
	message_content = 'AFRIEND' + '&' + name_receiver
	m = Message(publisher_id = 0, receiver_id = id_sender, type = 'AFRIEND', content = message_content)
	m.save()

def m_naFriend(message):
	id_receiver, name_sender = message.split('_')
	id_sender = getIdByName(name_sender)
	name_receiver = getNameById(id_receiver)
	message_content = 'NAFRIEND' + '&' + name_receiver
	m = Message(publisher_id = 0, receiver_id = id_sender, type = 'NAFRIEND', content = message_content)
	m.save()

def m_rRegret(message):
	id_sender = eval(message)
	id_room = getRoomidByid(id_sender)
	roomins = Room.objects.get(id = id_room)
	roomins.game_state = 'pause'
	roomins.pausestart = datetime.now()
	roomins.save()
	g_rRegret(id_sender, id_room)

def m_aRegret(message):
	id_sender = eval(message)
	id_room = getRoomidByid(id_sender)
	g_aRegret(id_sender, id_room)

def m_naRegret(message):
	id_sender = eval(message)
	id_room = getRoomidByid(id_sender)
	g_naRegret(id_sender, id_room)

def m_rTie(message):
	id_sender = eval(message)
	id_room = getRoomidByid(id_sender)
	roomins = Room.objects.get(id = id_room)
	roomins.game_state = 'pause'
	roomins.pausestart = datetime.now()
	roomins.save()
	g_rTie(id_sender, id_room)

def m_aTie(message):
	id_sender = eval(message)
	id_room = getRoomidByid(id_sender)
	g_aTie(id_sender, id_room)

def m_naTie(message):
	id_sender = eval(message)
	id_room = getRoomidByid(id_sender)
	g_naTie(id_sender, id_room)

def m_enterRoom(message):
	id_sender, id_room, role = message.split('_')
	roomins = Room.objects.get(id = id_room)
	if role == '1':
		roomins.owner_id = id_sender
	else:
		roomins.guest_id = id_sender
	roomins.last_steptime = datetime.now()
	roomins.pausestart = datetime.now()
	roomins.save()
	players = ChessPlayer.objects.filter(game_state = 'online')
	for player in players:
		content = 'ENTERROOM' + '&' + id_sender + '_' + id_room + '_' + role
		m = Message(publisher_id = 0, receiver_id = player.id, type = 'ENTERROOM', content = content)
		m.save()

def m_gg(message):
	id_self, id_enemy, id_room = message.split('_')
	g_EndGame(False, id_enemy, id_self, id_room)



