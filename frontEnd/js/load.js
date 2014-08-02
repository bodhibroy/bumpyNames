var canvas;
var context;
var HEIGHT=25, WIDTH=40;
var dx=32,dy=32;
var serverIP='192.168.0.12:8000';
window.addEventListener('keydown',performKeyDownEvent,true);

var game_state = null
var message_queue = []

function startView(){
	canvas=document.getElementById("myCanvas");
	context=canvas.getContext('2d');
	var ip='';
	draw();
	reDraw();
}


function draw() {
	context.beginPath();
	context.clearRect(0, 0, WIDTH, HEIGHT);
	drawALL();
	context.closePath();
}

function drawALL(){
    $.getJSON('http://'+ serverIP+ '/game_state/', function(data) {
    //data is the JSON string
	var players=data['players'];
	for (var player in players){
	    var iconURL='http://'+ serverIP+ '/icons/' + players[player]['icon'];
	    var pos_x=players[player]['location_x'] * dx;
	    var pos_y=players[player]['location_y'] * dy;
	    var img = new Image;
	    img.src = iconURL;
	    context.drawImage(img,pos_x,pos_y);
	}
    });
    
}

function performKeyDownEvent(event){
	move = ''
	switch (event.keyCode){
		case 38:  /* Up arrow was pressed */
			move = 'UP'
		break;
		case 40:  /* Down arrow was pressed */
			move = 'DOWN'
		break;
		case 37:  /* Left arrow was pressed */
			move = 'LEFT'
		break;
		case 39:  /* Right arrow was pressed */
			move = 'RIGHT'
		break;
	}
	console.log(move)
	if (move != '') {
		$.getJSON('/move/' + move, function(data){
			game_state = data.game_state
		});
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

$.getJSON('/game_state', function(data){
	game_state = data
});