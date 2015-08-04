			var roomid = 2;
			var img_mychess;
			var consult_per_second = 1;
			var messageToSend = [];
			var chessboard;
			var mycanvas;
			var myctx;
			mychess = new Image();
			mychess.src = ""
			function messageLoop(){
				message = messageToSend.join();
				//console.log(message);
				messageToSend = [];
				$.ajax({url: "message/" + selfid + '@' + message, success: function(result){
					//console.info(result);
					messageToHandle = result.split(",");
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
							sender_rfriend_name = body.split(' ')[1];
							alert(body + "jia ni le");
							break;
						case 'NAFRIEND':
							sender_rfriend_id = body.split('_')[0];
							sender_rfriend_name = body.split(' ')[1];
							alert(body + 'ju jue le ni');
							break;
						case 'AFRIEND':
							sender_rfriend_id = body.split('_')[0];
							sender_rfriend_name = body.split(' ')[1];
							alert(body + 'jie shou le ni de hao you qing qiu');
							break;
						}
					});
				}});
			};
			function addMessage(m){
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
				}
				messageToSend.push(message);
			};
			window.onload = function(){
				mycanvas = document.getElementById('canvas');
				myctx = mycanvas.getContext('2d');
				if (mycolor == 2){
					img_mychess = $('#whitechess');
				} else {
					img_mychess = $('#blackchess');
				}
				$(window).click(function(e){
					if (!ifmyturn){
						return;
					}
					var x = e.clientX - delta - parseInt($('#canvas').css('left'));
					var y = e.clientY - delta - parseInt($('#canvas').css('top'));
					x = x + gridwidth / 2;
					y = y + gridwidth / 2;
					x_index = Math.floor(x / gridwidth);
					y_index = Math.floor(y / gridwidth);
					img_x = x_index * gridwidth - gridwidth / 2 + delta;
					img_y = y_index * gridwidth - gridwidth / 2 + delta;
					if (x_index < 0 || x_index > 14 || y_index < 0 || y_index > 14){
						return;
					}
					if (chessboard[y_index][x_index] != 0){
						return;
					}
					chessboard[y_index][x_index] = mycolor;
					if (mycolor == 2){
						myctx.drawImage(whitechess, img_x, img_y, gridwidth, gridwidth);
					}else{
						myctx.drawImage(blackchess, img_x, img_y, gridwidth, gridwidth);
					}
					addMessage({type: 'ONESTEP', x: x_index, y: y_index});
					ifmyturn = false;
				});
				$(window).mousemove(function(e){
					if (!ifmyturn){
						return;
					}
					var x = e.clientX - delta - parseInt($('#canvas').css('left'));
					var y = e.clientY - delta - parseInt($('#canvas').css('top'));
					x = x + gridwidth / 2;
					y = y + gridwidth / 2;
					x_index = Math.floor(x / gridwidth);
					y_index = Math.floor(y / gridwidth);
					img_x = x_index * gridwidth - gridwidth / 2 + delta + parseInt($('#canvas').css('left'));
					img_y = y_index * gridwidth - gridwidth / 2 + delta + parseInt($('#canvas').css('top'));
					img_mychess.css('left', img_x.toString() + 'px');
					img_mychess.css('top', img_y.toString() + 'px');
					if (x_index < 0 || x_index > 14 || y_index < 0 || y_index > 14){
						img_mychess.css('visibility', 'hidden');
						return;
					}
					if (chessboard[y_index][x_index] != 0){
						img_mychess.css('visibility', 'hidden');
						return;
					}
					img_mychess.css('visibility', 'visible');
				});
				chessboard = new Array(15);
				for (var i = 0; i < 15; i++){
					chessboard[i] = new Array(15);
					for (var j = 0; j < 15; j++){
						chessboard[i][j] = 0;
					}
				}
				setInterval(messageLoop, 1000 / consult_per_second);
			};
			function printboard(){
				for (var i = 0; i < 15; i++){
					console.info(JSON.stringify(chessboard[i]));
				}
			}
			