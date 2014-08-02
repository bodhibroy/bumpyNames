var canvas;
var context;
var HEIGHT=18, WIDTH=37;
var dx=32,dy=32;

window.addEventListener('keydown',performKeyDownEvent,true);


var me = null
var game_state = null
var message_queue = []

var active_move = false

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
function playSound(filename, volume) {
	var snd = new Audio("/sounds/" + filename); // buffers automatically when created
	snd.volume = volume
	snd.play();
}
// ------------------------------------------------------
// ------------------------------------------------------


function updateGameState(){
    $.getJSON('/game_state', function(data){
    	if (data != null) {
			game_state = data
			me = data.me
			// Populate Message Queue
			if (game_state != null) {
				for (var i = 0; i < game_state.messages.length; i++) {
					message_queue.push(game_state.messages[i])
				}
				game_state.messages = []
			}

			processMessages()
			updateScores();
			draw()
		}
	});
}

function processMessages() {
	msg = message_queue
	message_queue = []

	for (var i = 0; i < msg.length; i++) {
		game_messages = []
		game_messages[1] = "user move"
		game_messages[2] = "collide"
		game_messages[3] = "collided into"
		game_messages[4] = "collected coin"
		console.log(game_messages[msg[i].message])
		switch (msg[i].message){
			case 1:
				// game_messages["user move"] = 1
				playSound(getMoveSound(), 0.5)
			break;
			case 2:
				// game_messages["collide"] = 2
				playSound(getCollideSound(), 1)
			break;
			case 3:
				// game_messages["collided into"] = 3
				playSound(getCollidedIntoSound(), 1)
			break;
			case 4:
				// game_messages["collected coin"] = 4
				playSound(getCollectCoinSound(), 1)
			break;
		}
	}

	// ****** BODHI!!!! *****
	// Play sounds and other things
	// ****** BODHI!!!! *****
}


function draw() {
	context.beginPath();
	context.clearRect(0*dx, 0*dy, (WIDTH+1)*dx, (HEIGHT+1)*dy);

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
	if (active_move || (me == null)) {
		return
	}

	for (var i = 0; i < game_state.game.length; i++) {
		if (game_state.game[i].property == "game stop") {
			return
		}
	}

	move = ''
	switch (event.keyCode){
		case 38:  /* Up arrow was pressed */
			if (me.location_y + 1 <= HEIGHT) {
				move = 'UP'
			}
		break;
		case 40:  /* Down arrow was pressed */
			if (me.location_y - 1 >= 0) {
				move = 'DOWN'
			}
		break;
		case 37:  /* Left arrow was pressed */
			if (me.location_x - 1 >= 0) {
				move = 'LEFT'
			}
		break;
		case 39:  /* Right arrow was pressed */
			if (me.location_x + 1 <= WIDTH) {
				move = 'RIGHT'
			}
		break;
	}
	if (move != '') {
		active_move = true
		$.getJSON('/move/' + move, function(data){
			game_state = data.game_state

			if (game_state != null) {
				for (var i = 0; i < game_state.messages.length; i++) {
					message_queue.push(game_state.messages[i])
				}
				game_state.messages = []
			}

			active_move = false

			// ****** BODHI!!!! *****
			// do something about the details?
			// ****** BODHI!!!! *****
		});
	}
}


function restartGame(){
	window.location.href='./index.html';
}

function updateScores(){
	var leaderBoard=document.getElementById('ldb');
	// update LeaderBoard
	var coins=[]
	var playersList=game_state.players
	for (var i=0; i< playersList.length; i++){
		coins.push({ip: playersList[i].ip,name: playersList[i].name,coins: playersList[i].coins})
	}
	finalScores=coins.sort(function (o1,o2){
		return o1.coins-o2.coins;
	});
}


updateGameState()

function startView() {
	canvas=document.getElementById("myCanvas");
	context=canvas.getContext('2d');
	setInterval(updateGameState, 100);
}
