var canvas;
var context;
var HEIGHT=25, WIDTH=40;
var dx=32,dy=32;
// var x=200,y=60;
// var runAnimation=true;
// var bbby=100;
// var bbbx=WIDTH/2-50;
// var flag=1;
// var name=document.cookie.split('=')[1].toUpperCase();
// var ip='';

window.addEventListener('keydown',performKeyDownEvent,true);

// function getBBBX(){
// 	return bbbx;
// }
// 
// function getBBBY(){
// 	if (bbby==HEIGHT-200)
// 		flag=-1;
// 	else if (bbby<0)
// 		flag=1;
// 	if (flag==1)
// 		bbby+=20;
// 	else
// 		bbby-=20;
// 	return bbby;
// }

function startView(){
	if(document.cookie.split('=')[1]){
// 		name=document.cookie.split(';')[0].split('=')[1];
		canvas=document.getElementById("myCanvas");
		context=canvas.getContext('2d');
		var ip='';
		draw();
		reDraw();
	}
	else{alert("Very funny lah! You didn't put in your name.");restartGame()};
}


function draw() {
	if (runAnimation){
		context.beginPath();
		context.clearRect(0, 0, WIDTH, HEIGHT);
		drawALL(); 
		// draw BBB block
		// context.fillStyle = 'red';
// 		context.font="20px Serif bold";
// 		context.fillText('Burning Box', getBBBX()+15, getBBBY()+90);
// 
// 		context.rect(getBBBX(), getBBBY(), 130,220);
// 		
// 		
// 		context.strokeStyle = 'black';
// 		context.stroke();
// 		context.closePath();
		// context.beginPath();
// 		context.arc(WIDTH/2 - 60, HEIGHT/2, 50,0,2*Math.PI);
// 		context.fillStyle = '#00FFFF';
// 		context.fill();
// 		context.lineWidth = 7;
// 		context.strokeStyle = 'black';
// 		context.stroke();
// 		context.closePath();
		// Draw players

// 		drawALL(); 

		//drawOthers(); 
		
		
	}
}

function drawALL(){
    $.getJSON('http://localhost:8000/game_state', function(data) {
    //data is the JSON string
	//console.log(data);
	var players=data['players'];
	//console.log(players)
	for (var player in players){
	    //console.log(players[player]['icon']);
	    var iconURL='http://localhost:8000/icons/' + players[player]['icon'];
	    var pos_x=players[player]['location_x'];
	    var pos_y=players[player]['location_y'];
	    var img = new Image;
	    img.src = iconURL;
	    context.drawImage(img,pos_x,pos_y);
	}
	//console.log('blah');

    });
    
}



// function drawEach(){
// 	var urlIcon=document.cookie.split(';')[0].split('=')[1];
// // 	console.log(urlIcon);
// // 	console.log('blah');
// }

// 
// function drawEach(){
// 
// // 	console.log(x,y);
// 	context.beginPath();
// // 	context.rect(x, y, Math.round(context.measureText(name).width)+10, 25);
// // 	context.arc(x,y,context.measureText(name).width/2+10,0,2*Math.PI);
// // 	context.fillStyle = '#FFFFFF';
// // 	context.fill();
// // 	context.lineWidth = 3;
// // 	context.strokeStyle = colorStroke;
// // 	context.stroke();
// // 	context.closePath();
// // 	context.beginPath();
// // 	if (document.cookie.split('=')[1].toUpperCase()!=name){
// // 		context.font="17px Serif";
// // 		context.fillStyle='#000000';
// // 	}
// // 	else{
// // 		context.font="20px Serif";
// // 		context.fillStyle='#FF0000';
// // 	}
// // 	context.fillText(name, x-Math.round(context.measureText(name).width/2), y+5);
// 	
// 	context.closePath();
// 	
// }

// function drawOthers(names){
// // draw others as and when they join the game
// 	for (var i =0; i < names.length; i++){
// 		// draw the others
// 		// drawEach(names[i], 'white', 'black');
// 	}
// }

function performKeyDownEvent(event){
	switch (event.keyCode){
		case 38:  /* Up arrow was pressed */
			if (y - dy > 0){
				y -= dy;
				
			}
		break;
		case 40:  /* Down arrow was pressed */
			if (y + dy < HEIGHT){
				y += dy;
				
			}
		break;
		case 37:  /* Left arrow was pressed */
			if (x - dx-10> 0){
				x -= dx;
				
			}
		
		break;
		case 39:  /* Right arrow was pressed */
			if (x + dx  < WIDTH){
				x += dx;
			}
		break;
	}
}


function restartGame(){
	window.location.href='./index.html';
}


function reDraw(){
	return setInterval(draw, 100);
}

function updateScores(){
	var leaderBoard=document.getElementById('ldb');
	// update LeaderBoard
}
