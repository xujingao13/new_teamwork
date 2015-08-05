			var roomid = 2;
			var img_mychess;
			var consult_per_second = 1;
			var messageToSend = [];
			var chessboard;
			var mycanvas;
			var myctx;
			var sender_rfriend_id;
			var sender_rfriend_name;
			var roomlist;
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
							break;
						case 'RGAMESTART':
							console.log('rgamestart');
							break;
						case 'GAMESTART':
							console.log('gamestart');
							if(ifowner){
								ifmyturn = true;
							}else{
								ifmyturn = false;
							}
							break;
						case 'WIN':
							alert('win');
							break;
						case 'LOSE':
							alert('lose');
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
							$('#time').html(body);
							break;
						case 'RREGRET':
							console.log('RREGRET' + body);
							break;
						case 'AREGRET':
							console.log('AREGRET' + body);
							break;
						case 'NAREGRET':
							console.log('NAREGRET' + body);
							break;
						case 'RTIE':
							console.log('RTIE' + body);
							break;
						case 'TIE':
							console.log('TIE' + body);
							break;
						case 'NATIE':
							console.log('NATIE' + body);
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
							enemyid = eval(body);
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
			