from player.models import *
from othermodule.game import *
from othermodule.userinfo import *

def m_oneStep(message):
	x, y, id_self, id_enemy, id_room = [eval(i) for i in message.split('_')]
	currentroom = Room.objects.get(id = id_room)
	currentroom.whose_turn = id_enemy
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
	g_gameStart(id_room)

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
	message_content = 'AFRIEND' + name_receiver
	m = Message(publisher_id = 0, receiver_id = id_sender, type = 'AFRIEND', content = message_content)
	m.save()

