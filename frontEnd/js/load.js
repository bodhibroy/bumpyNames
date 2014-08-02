var canvas;
var context;
var HEIGHT=25, WIDTH=40;
var dx=32,dy=32;
var serverIP='192.168.0.12:8000';
window.addEventListener('keydown',performKeyDownEvent,true);

function startView(){
	if(document.cookie.split('=')[1]){
		canvas=document.getElementById("myCanvas");
		context=canvas.getContext('2d');
		var ip='';
		draw();
		reDraw();
	}
	else{alert("Very funny lah! You didn't put in your name.");restartGame()};
}


function draw() {
	context.beginPath();
	context.clearRect(0, 0, WIDTH, HEIGHT);
	drawALL();
}

function drawALL(){
    $.getJSON('http://'+ serverIP+ '/game_state/', function(data) {
    //data is the JSON string
	var players=data['players'];
	for (var player in players){
	    var iconURL='http://'+ serverIP+ '/icons/' + players[player]['icon'];
	    var pos_x=players[player]['location_x'];
	    var pos_y=players[player]['location_y'];
	    var img = new Image;
	    img.src = iconURL;
	    context.drawImage(img,pos_x,pos_y);
	}
    });
    
}

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
