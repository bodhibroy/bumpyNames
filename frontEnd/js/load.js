var canvas;
var context;
var HEIGHT=18, WIDTH=37;
var dx=32,dy=32;

window.addEventListener('keydown',performKeyDownEvent,true);


var game_state = null
var message_queue = []


// ------------------------------------------------------
// Getting resource URLS
// ------------------------------------------------------
var coin_icon = 'coins_stack.png'
$.getJSON('/get_coin_icon', function(data){
	if (data.coin_icon != null) {
		coin_icon = data.coin_icon
	}
});

var collide_into_sounds = []
$.getJSON('/get_sound_list/gruntA', function(data){
	if (data.sounds != null) {
		collide_into_sounds = data.sounds
	}
});
function getCollideSound() {
	return randomArrayElement(collide_into_sounds)
}

var collided_into_sounds = []
$.getJSON('/get_sound_list/gruntB', function(data){
	if (data.sounds != null) {
		collided_into_sounds = data.sounds
	}
});
function getCollidedIntoSound() {
	return randomArrayElement(collided_into_sounds)
}

var collect_coin_sounds = []
$.getJSON('/get_sound_list/money', function(data){
	if (data.sounds != null) {
		collect_coin_sounds = data.sounds
	}
});
function getCollectCoinSound() {
	return randomArrayElement(collect_coin_sounds)
}

var move_sounds = []
$.getJSON('/get_sound_list/move', function(data){
	if (data.sounds != null) {
		move_sounds = data.sounds
	}
});
function getMoveSound() {
	return randomArrayElement(move_sounds)
}

function randomArrayElement(arr) {
	return arr[Math.floor(Math.random()*arr.length)]
}
// ------------------------------------------------------
// ------------------------------------------------------


function updateGameState(){
    $.getJSON('/game_state', function(data){
		game_state = data

		// Populate Message Queue
		if (game_state != null) {
			for (var i = 0; i < game_state.messages.length; i++) {
				message_queue.push(game_state.messages[i])
			}
			game_state.messages = []
		}

		processMessages()
		updateLeaderBoard();
		draw()
	});
}

function processMessages() {
	// ****** BODHI!!!! *****
	// Play sounds and other things
	// ****** BODHI!!!! *****
}


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

	if (game_state != null) {
		var players = game_state['players'];
		for (var player in players){
		    var iconURL='/icons/' + players[player]['icon'];
		    var pos_x=players[player]['location_x'] * dx;
		    var pos_y=(HEIGHT - players[player]['location_y']) * dy;
		    var img = new Image;
		    img.src = iconURL;
		    context.drawImage(img,pos_x,pos_y);
		}
    }

	if (game_state != null) {
		for (var player in game_state['players']){
		    var iconURL='/icons/' + game_state['players'][player]['icon'];
		    var pos_x=game_state['players'][player]['location_x'] * dx;
		    var pos_y=(HEIGHT - game_state['players'][player]['location_y']) * dy;
		    var img = new Image;
		    img.src = iconURL;
		    context.drawImage(img,pos_x,pos_y);
		}

		for (var coin in game_state['coins']){
		    var iconURL='/icons/' + coin_icon;
		    var pos_x=game_state['coins'][coin]['location_x'] * dx;
		    var pos_y=(HEIGHT - game_state['coins'][coin]['location_y']) * dy;
		    var img = new Image;
		    img.src = iconURL;
		    context.drawImage(img,pos_x,pos_y);
		}
    }

	context.closePath();
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

			// ****** BODHI!!!! *****
			// do something about the details?
			console.log('Attempting to move ' + move)
			console.log(data.success)
			console.log(data.details)
			// ****** BODHI!!!! *****
		});
	}
}


function restartGame(){
	window.location.href='./index.html';
}


function reDraw(){
	return setInterval(updateGameState, 100);
}

function updateScores(){
	var leaderBoard=document.getElementById('ldb');
	// update LeaderBoard
	var coins=[]
	var playersList=game_state.players
	for (var i=0; i< playersList.length; i++){
					coins.push({ip=playersList[i].ip,name=playersList[i].name,coins=playersList[i].coins})
	}
	finalScores=coins.sort(function (o1,o2){
		return o1.coins-o2.coins;
	});
}

updateGameState()
