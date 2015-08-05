from player.models import *

def g_gameStart(id_room):
	room = Room.objects.get(id = id_room)
	owner = room.owner_id
	guest = room.guest_id
	room.whose_turn = owner
	room.game_state = 'gaming'
	room.chess_board = '0'*225
	room.last_chess_board = '0'*225
	room.save()

def g_getIndex(x, y):
	return x + y * 15

def g_ifGameOver(newChessboard, x, y, color):#0:continue 1:color win
	c_x = x
	c_y = y
	up = 0
	down = 0
	left = 0
	right = 0
	lu = 0
	ru = 0
	ld = 0
	rd = 0
	while True:
		c_y -= 1
		if c_y >= 0 and newChessboard[g_getIndex(c_x, c_y)] == color:
			up += 1
		else:
			break
	c_x = x
	c_y = y
	while True:
		c_y += 1
		if c_y <= 14 and newChessboard[g_getIndex(c_x, c_y)] == color:
			down += 1 
		else:
			break
	c_x = x
	c_y = y
	while True:
		c_x -= 1
		if c_x >= 0 and newChessboard[g_getIndex(c_x, c_y)] == color:
			left += 1
		else:
			break
	c_x = x
	c_y = y
	while True:
		c_x += 1
		if c_x <= 14 and newChessboard[g_getIndex(c_x, c_y)] == color:
			right += 1
		else:
			break
	c_x = x
	c_y = y
	while True:
		c_y -= 1
		c_x -= 1
		if c_y >= 0 and c_x >= 0 and newChessboard[g_getIndex(c_x, c_y)] == color:
			lu += 1
		else:
			break;
	c_x = x
	c_y = y
	while True:
		c_y -= 1
		c_x += 1
		if c_y >= 0 and c_x <= 14 and newChessboard[g_getIndex(c_x, c_y)] == color:
			ru += 1
		else:
			break
	c_x = x
	c_y = y
	while True:
		c_y += 1
		c_x -= 1
		if c_y <= 14 and c_x >= 0 and newChessboard[g_getIndex(c_x, c_y)] == color:
			ld += 1
		else:
			break
	c_x = x
	c_y = y
	while True:
		c_y += 1
		c_x += 1
		if c_y <= 14 and c_x <= 14 and newChessboard[g_getIndex(c_x, c_y)] == color:
			rd += 1
		else:
			break
	print (up, down, left, right, lu, rd, ld, ru)
	if up + down >= 4 or left + right >= 4 or lu + rd >= 4 or ld + ru >= 4:
		return 1
	else:
		return 0

def g_EndGame(ifTie, winner, loser, room):
	if not ifTie:
		m = Message(publisher_id = 0, receiver_id = winner, type = 'WIN', content = 'WIN')
		m.save()
		m = Message(publisher_id = 0, receiver_id = loser, type = 'LOSE', content = 'LOSE')
		m.save()
		"""
		user_win = ChessPlayer.objects.get(id = winner)
		user_lose = ChessPlayer.objects.get(id = loser)
		user_win.game_num += 1
		user_lose.game_num += 1
		user_win.game_grade += 3
		"""
	else:
		m = Message(publisher_id = 0, receiver_id = winner, type = 'TIE', content = '')
		m.save()
		m = Message(publisher_id = 0, receiver_id = loser, type = 'TIE', content = '')
		m.save()
		"""
		user_win = ChessPlayer.objects.get(id = winner)
		user_lose = ChessPlayer.objects.get(id = loser)
		user_win.game_num += 1
		user_lose.game_num += 1
		user_win.game_grade += 1
		user_lose.game_grade += 1
		"""
