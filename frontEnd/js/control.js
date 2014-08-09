var COIN_COUNTDOWN_INTERVAL = 10

var game_stopped = false

var coin_count_down = 10000
function coinLoop() {
	coin_count_down -= COIN_COUNTDOWN_INTERVAL
	
	if (coin_count_down <= 0) {
		pushCoin()
	}

	setTimeout(coinLoop, COIN_COUNTDOWN_INTERVAL)
}

function pushCoin(){
	$.getJSON('/game_state', function(data){
		game_state = data
		coins = game_state['coins']
		players = game_state['players']
		//var locations = []

		if (game_stopped) {
			return
		}
		
		var randomX=Math.floor(Math.random()*38);
		var randomY=Math.floor(Math.random()*19);
		
		var flag =0;
		for (var i=0;i<coins.length; i++){
			if (coins[i]['location_x'] == randomX && coins[i]['location_y'] == randomY)
				flag = 1;
				break;
		}
		if (flag==0)
		for (var player in players){
			if (player['location_x']==randomX && player['location_y']==randomY)
				flag = 1;
				break;
		}
		if (flag==0){
			var pushCoinURL='/add_coin/' + randomX + '/' + randomY + '/' + KING_B0DH1_PA55W0RD;
			console.log('Attempting to add coin at (' + randomX + ', ' + randomY + ')')
			$.getJSON(pushCoinURL);
		}
	});
	next_try_interval = getNextInterarrivalTime()
}


function validateFreq() {
	myFreq = document.someForm.freq.value
	if (myFreq.match(/^\d+$/g) == null) {
		document.someForm.freq.value = '2000'
	}
	if (parseInt(document.someForm.freq.value) <= 0) {
		document.someForm.freq.value = '2000'
	}
	coin_count_down = parseInt(document.someForm.freq.value)
	console.log('Next try in ' + (coin_count_down/1000.0) + ' sec')
}

function getNextInterarrivalTime() {
	validateFreq();
	return parseInt(document.someForm.freq.value);
}

function takeControlAction(url, actionDesc) {
	$.getJSON(url, function(data) {
		s = ''
		if ((data == null) || (data.success == false)) {
			s = "Failed to " + actionDesc + "."
		} else {
			s = "Successfully " + actionDesc + "."
		}
		alert(s)
		console.log('')
		console.log(s)
		console.log(data)
		console.log('')
	});
}

function setGameStateStop() {
	// url = '/set_game_state/Game%20Stop%2CFreeze%2C1%2C1/' + KING_B0DH1_PA55W0RD
	url = '/set_game_state/Game Stop,Freeze,0,0/' + KING_B0DH1_PA55W0RD
	actionDesc = 'Set game state to STOP'
	takeControlAction(url, actionDesc)
	game_stopped = true
}

function clearGameState() {
	// url = '/set_game_state/game%20on%2CThe%20show%20must%20go%20%2C1%2C1/' + KING_B0DH1_PA55W0RD
	url = '/set_game_state/Game On,The show must go on...,0,0/' + KING_B0DH1_PA55W0RD
	actionDesc = 'reset game state'
	takeControlAction(url, actionDesc)
	game_stopped = false
}

function clearCoinScoresAndMoves() {
	url = '/reset_scores/' + KING_B0DH1_PA55W0RD
	actionDesc = 'reset scores'
	takeControlAction(url, actionDesc)
}

function clearCoinsFromMap() {
	url = '/clear_coins/' + KING_B0DH1_PA55W0RD
	actionDesc = 'clear coins from map'
	takeControlAction(url, actionDesc)
}

function resetDB() {
	if(confirm('Really reset the DB?')) {
		url = '/clear_db/' + KING_B0DH1_PA55W0RD
		actionDesc = 'reset DB'
		takeControlAction(url, actionDesc)
	}
}




iconURL = ''
function imageClick(_src){
	iconURL=_src;
	document.getElementById('selectedIcon').innerHTML='<img src="' + iconURL + '">';
}
all_icons = []

$.getJSON('/get_icon_list', function(data) {
	if (data != null) {
		all_icons = data.icons
	} else {
		all_icons = ['Animal_Icons_alligator.png', 'Animal_Icons_ant.png', 'Animal_Icons_bat.png', 'Animal_Icons_bear.png', 'Animal_Icons_bee.png', 'Animal_Icons_bird.png', 'Animal_Icons_bull.png', 'Animal_Icons_bulldog.png', 'Animal_Icons_butterfly.png', 'Animal_Icons_cat.png', 'Animal_Icons_chicken.png', 'Animal_Icons_cow.png', 'Animal_Icons_crab.png', 'Animal_Icons_crocodile.png', 'Animal_Icons_deer.png', 'Animal_Icons_dog.png', 'Animal_Icons_donkey.png', 'Animal_Icons_duck.png', 'Animal_Icons_eagle.png', 'Animal_Icons_elephant.png', 'Animal_Icons_fish.png', 'Animal_Icons_fox.png', 'Animal_Icons_frog.png', 'Animal_Icons_giraffe.png', 'Animal_Icons_gorilla.png', 'Animal_Icons_hippo.png', 'Animal_Icons_horse.png', 'Animal_Icons_insect.png', 'Animal_Icons_lion.png', 'Animal_Icons_monkey.png', 'Animal_Icons_moose.png', 'Animal_Icons_mouse.png', 'Animal_Icons_owl.png', 'Animal_Icons_panda.png', 'Animal_Icons_penguin.png', 'Animal_Icons_pig.png', 'Animal_Icons_rabbit.png', 'Animal_Icons_rhino.png', 'Animal_Icons_rooster.png', 'Animal_Icons_shark.png', 'Animal_Icons_sheep.png', 'Animal_Icons_snake.png', 'Animal_Icons_tiger.png', 'Animal_Icons_turkey.png', 'Animal_Icons_turtle.png', 'Animal_Icons_wolf.png'];			
	}

	var content='<table border=\"1\">'
	var colsPerRow = 24
	for (var i=0;i<all_icons.length;i++) {
		if(i%colsPerRow==0) {
			content+='<tr>'
		}
		var temp='<td><img src=\"/icons/' + all_icons[i] + '\"'+ ' height="32" width="32" onclick="imageClick(this.src);"></td>'
		content+=temp
		if(i%colsPerRow==colsPerRow-1) {
			content+='</tr>'
		} else if (i==all_icons.length-1) {
			content+='</tr>'
		}
	}
	content+='</table>'
	//console.log(content)
	document.getElementById('icontable').innerHTML=content;
	imageClick('/icons/' + all_icons[Math.floor(Math.random()*all_icons.length)])
});



function bossInPlay() 
{
	if(document.someForm.username.value == "") 
	{
		alert("please enter a Name");
		return false;
	}
	if (iconURL=="")
	{
		alert("please choose an icon");
		return false;
	}
	else
	{
		var e = document.getElementById("race");
		var character = e.options[e.selectedIndex].value;
		e = document.getElementById("gender");
		var gender = e.options[e.selectedIndex].value;
		e = document.getElementById("class");
		var _class = e.options[e.selectedIndex].value;
		e = document.getElementById("race");
		var race = e.options[e.selectedIndex].value;
		// var icon = document.cookie.split(';')[0].split('=')[1].split('/')[4];

		var iconL = iconURL.split('/')
		var icon = iconL[iconL.length-1]

		var nameOfUser= document.someForm.username.value;
		nameOfUser.replace(/(\||\/)/g, '');

		var url='/add_or_update_user/' + nameOfUser + '/' + icon + '/' + gender + '/' + race + '/' + _class + '/4/34/3/15';

		$.getJSON(url, function(data) {
			if (data.success) {
				alert('Success.')
			} else {
				alert('Failed. (Huh!?)');
			}
		});
	}
}