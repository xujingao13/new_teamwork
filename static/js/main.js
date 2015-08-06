			var img_mychess;
			var consult_per_second = 1;
			var messageToSend = [];
			var chessboard;
			var mycanvas;
			var myctx;
			var sender_rfriend_id;
			var sender_rfriend_name;
			var roomlist;
			var lastx, lasty, lastx_index, lasty_index;
			mychess = new Image();
			mychess.src = ""
			function messageLoop(){
				message = messageToSend.join('+');
				//console.log(message);
				messageToSend = [];
				$.ajax({url: "message/" + selfid + '@' + message, success: function(result){
					//console.info(result);
					messageToHandle = result.split("+");
					messageToHandle.forEach(function(m){
						//console.info(m);
						var temp = m.split('&');
						head = temp[0];
						body = temp[1];
						switch(head){
						case 'ONESTEP':
							temp = body.split('_');
							var x = Number(temp[0]);
							var y = Number(temp[1]);
							chessboard[y][x] = enemycolor;
							ifmyturn = true;
							img_x = x * gridwidth - gridwidth / 2 + delta;
							img_y = y * gridwidth - gridwidth / 2 + delta;
							if (mycolor == 2){
								myctx.drawImage(blackchess, img_x, img_y, gridwidth, gridwidth);
							}else{
								myctx.drawImage(whitechess, img_x, img_y, gridwidth, gridwidth);
							}
							lastx = img_x;
							lasty = img_y;
							lastx_index = x;
							lasty_index = y;
							$('#regret').css('visibility', 'hidden');
							break;
						case 'RGAMESTART':
							console.log('rgamestart');
							$('#dc-title').html('房主请求开始游戏');
							$('#dc-body').html('房主请求开始游戏');
							$('#dc-accept').attr('onclick', 'agreeStart()');
							$('#dc-reject').attr('onclick', 'rejectStart()');
							$('#dc-btn').trigger('click');
							break;
						case 'GAMESTART':
							console.log('gamestart');
							if(ifowner){
								ifmyturn = true;
							}else{
								ifmyturn = false;
							}
							break;
						case 'NAGAMESTART':
							$('#sc-title').html('对方不同意开始游戏');
							$('#sc-body').html('对方不同意开始游戏');
							$('#sc-btn').trigger('click');
							break;
						case 'WIN':
							console.log('WIN' + body);
							$('#sc-title').html('You Win');
							$('#sc-body').html('你赢了');
							$('#sc-btn').trigger('click');

							myctx.clearRect(0, 0, 537, 537);
							chessboard = new Array(15);
							for (var i = 0; i < 15; i++){
								chessboard[i] = new Array(15);
								for (var j = 0; j < 15; j++){
									chessboard[i][j] = 0;
								}
							}
							ifmyturn = false;
							$('#selftime').html('60s');
							$('#enemytime').html('60s');
							img_mychess.css('visibility', 'hidden');
							break;
						case 'LOSE':
							console.log('LOSE' + body);
							$('#sc-title').html('You Lose');
							$('#sc-body').html('你输了');
							$('#sc-btn').trigger('click');

							myctx.clearRect(0, 0, 537, 537);
							chessboard = new Array(15);
							for (var i = 0; i < 15; i++){
								chessboard[i] = new Array(15);
								for (var j = 0; j < 15; j++){
									chessboard[i][j] = 0;
								}
							}
							img_mychess.css('visibility', 'hidden');
							ifmyturn = false;
							$('#selftime').html('60s');
							$('#enemytime').html('60s');
							break;
						case 'RFRIEND':
							sender_rfriend_id = body.split('_')[0];
							sender_rfriend_name = body.split('_')[1];
							$('#rf-sender').html(sender_rfriend_name + "请求添加您为好友");
							$('#btn-addfrd').trigger('click');
							break;
						case 'NAFRIEND':
							$('#rplfrd').html(body + '拒绝了您的好友请求');
							$('#btn-rplfrd').trigger('click');
							break;
						case 'AFRIEND':
							$('#rplfrd').html(body + '接受了您的好友请求');
							$('#btn-rplfrd').trigger('click');
							break;
						case 'TIME':
							var time = Math.floor(Number(body)/1000);
							if (ifmyturn){
								$('#selftime').html(time + 's');
								$('#enemytime').html('');
							} else {
								$('#selftime').html('');
								$('#enemytime').html(time + 's');
							}
							break;
						case 'RREGRET':
							console.log('RREGRET' + body);
							$('#dc-title').html('对方请求悔棋');
							$('#dc-body').html('对方请求悔棋');
							$('#dc-accept').attr('onclick', 'agreeRegret()');
							$('#dc-reject').attr('onclick', 'rejectRegret()');
							$('#dc-btn').trigger('click');
							break;
						case 'AREGRET':
							console.log('AREGRET' + body);
							ifmyturn = true;
							myctx.clearRect(lastx, lasty, gridwidth, gridwidth);
							chessboard[lasty_index][lastx_index] = 0;
							$('#regret').css('visibility', 'hidden');
							$('#sc-title').html('对方同意您悔棋');
							$('#sc-body').html('对方同意您悔棋');
							$('#sc-btn').trigger('click');
							break;
						case 'NAREGRET':
							console.log('NAREGRET' + body);
							$('#sc-title').html('对方不同意您悔棋');
							$('#sc-body').html('对方不同意您悔棋');
							$('#sc-btn').trigger('click');
							break;
						case 'RTIE':
							console.log('RTIE' + body);
							$('#dc-title').html('对方请求和棋');
							$('#dc-body').html('对方请求和棋');
							$('#dc-accept').attr('onclick', 'agreeTie()');
							$('#dc-reject').attr('onclick', 'rejectTie()');
							$('#dc-btn').trigger('click');
							break;
						case 'TIE':
							console.log('TIE' + body);
							$('#sc-title').html('和棋');
							$('#sc-body').html('不输不赢');
							$('#sc-btn').trigger('click');
							img_mychess.css('visibility', 'hidden');
							myctx.clearRect(0, 0, 537, 537);
							chessboard = new Array(15);
							for (var i = 0; i < 15; i++){
								chessboard[i] = new Array(15);
								for (var j = 0; j < 15; j++){
									chessboard[i][j] = 0;
								}
							}
							ifmyturn = false;
							$('#selftime').html('60s');
							$('#enemytime').html('60s');
							break;
						case 'NATIE':
							console.log('NATIE' + body);
							$('#sc-title').html('对方不同意和棋');
							$('#sc-body').html('对方不同意和棋');
							$('#sc-btn').trigger('click');
							break;
						case 'ROOMINFO':
							console.log(body);
							roomlist = eval(body);
							showRoomInfo();
							break;
						case 'ENTERROOM':
							console.log(2);
							var temp_list = body.split('_');
							enterRoom(temp_list[0], temp_list[1], temp_list[2]);
							break;
						case 'ENEMY':
							console.log('enemy' + body);
							var temp = body.split('_');
							enemyid = eval(temp[0]);
							enemyimg = temp[1];
							enemyname = temp[2];
							$('#enemyname').html(enemyname);
							$('#enemyimg').attr("src",enemyimg);
							break;
						case 'EXITROOM':
							var temp_list = body.split('_');
							exitRoom(temp_list[0], temp_list[1]);
							break;
						}
					});
				}});
			};
			function addMessage(m){
				console.log(m);
				switch(m.type){
				case 'ONESTEP':
					message = m.type + '&' + m.x + '_' + m.y + '_' + selfid + '_' + enemyid + '_' + roomid;
					break;
				case 'RGAMESTART':
					message = m.type + '&' + selfid + '_' + enemyid + '_' + roomid;
					break;
				case 'AGAMESTART':
					message = m.type + '&' + selfid + '_' + enemyid + '_' + roomid;
					break;
				case 'AFRIEND':
					message = m.type + '&' + selfid + '_' + m.sender;
					break;
				case 'RFRIEND':
					message = m.type + '&' + selfid + '_' + m.receiver;
					break;
				case 'AFRIEND':
					message = m.type + '&' + selfid + '_' + m.sender;
					break;
				case 'NAFRIEND':
					message = m.type + '&' + selfid + '_' + m.sender;
					break;
				case 'RREGRET':
					message = m.type + '&' + selfid;
					break;
				case 'AREGRET':
					message = m.type + '&' + selfid;
					break;
				case 'NAREGRET':
					message = m.type + '&' + selfid;
					break;
				case 'RTIE':
					message = m.type + '&' + selfid;
					break;
				case 'ATIE':
					message = m.type + '&' + selfid;
					break;
				case 'NATIE':
					message = m.type + '&' + selfid;
					break;
				case 'ROOMINFO':
					message = m.type + '&' + selfid;
					break;
				case 'ENTERROOM':
					console.log(1);
					message = m.type + '&' + selfid + '_' + m.roomid + '_' + m.role;
					break;
				case 'NAGAMESTART':
					message = m.type + '&' + enemyid;
					break;
				case 'GG':
					message = m.type + '&' + selfid + '_' + enemyid + '_' + roomid;
					break;
				}
				messageToSend.push(message);
			};
			function showRoomInfo(){
				for (var i = 1; i <= 18; i++){
					 if (roomlist[i].owner != 0){
					 	var x = Math.floor((i - 1) / 3);
					 	var y = (i - 1) % 3;
					 	$('#' + x + y + '1').attr('src', userimg[roomlist[i].owner]);
					 }
					 if (roomlist[i].guest != 0){
					 	var x = Math.floor((i - 1) / 3);
					 	var y = (i - 1) % 3;
					 	$('#' + x + y + '2').attr('src', userimg[roomlist[i].guest]);
					 }
				}
			};
			function enterRoom(id_player, id_room, role){
				if (typeof(roomlist) == 'undefined'){
					return;
				}
				if(role == '1'){
					roomlist[id_room].owner = id_player;
					var x = Math.floor((id_room - 1) / 3);
					var y = (id_room - 1) % 3;
					$('#' + x + y + '1').attr('src', userimg[id_player]);
				} else {
					roomlist[id_room].guest = id_player;
					var x = Math.floor((id_room - 1) / 3);
					var y = (id_room - 1) % 3;
					$('#' + x + y + '2').attr('src', userimg[id_player]);
				}

			};
			function exitRoom(id_player, id_room){
				if (typeof(roomlist) == 'undefined'){
					return;
				}
				roomlist[id_room].owner = id_player;
				var x = Math.floor((id_room - 1) / 3);
				var y = (id_room - 1) % 3;
				$('#' + x + y + '2').attr('src', '../static/images/nobody.jpg')
				if(id_player == '0'){
					$('#' + x + y + '1').attr('src', '../static/images/nobody.jpg');
				} else {
					$('#' + x + y + '1').attr('src', userimg[id_player]);
				}

			};
