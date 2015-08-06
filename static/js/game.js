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
					if (isNaN(x_index)){
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
					$('#regret').css('visibility', 'visible');
					lastx = img_x;
					lasty = img_y;
					lastx_index = x_index;
					lasty_index = y_index;
					ifmyturn = false;
				});
				$(window).mousemove(function(e){
					if (!ifmyturn){
						return;
					}
					var x = e.clientX - delta - $('#canvas').offset().left;
					var y = e.clientY - delta - $('#canvas').offset().top;
					x = x + gridwidth / 2;
					y = y + gridwidth / 2;
					x_index = Math.floor(x / gridwidth);
					y_index = Math.floor(y / gridwidth);
					img_x = x_index * gridwidth - gridwidth / 2 + delta + $('#canvas').offset().left;
					img_y = y_index * gridwidth - gridwidth / 2 + delta + $('#canvas').offset().top;
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