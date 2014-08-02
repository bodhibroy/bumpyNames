function pushCoin(){
	$.getJSON('/game_state', function(data){
		game_state = data
		coins = game_state['coins']
		players = game_state['players']
		//var locations = []
		
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
			var pushCoinURL='/add_coin/' + randomX + '/' + randomY + '/';
			console.log('Attempting to add coin at (' + randomX + ', ' + randomY + ')')
			$.getJSON(pushCoinURL);
		}
	});
	next_try_interval = getNextInterarrivalTime()
	console.log('Next try in ' + (next_try_interval/1000.0) + ' sec')
	setTimeout(pushCoin, next_try_interval);
	
}


function validateFreq() {
	myFreq = document.someForm.freq.value
	if (myFreq.match(/^\d+$/g) == null) {
		document.someForm.freq.value = '2000'
	}
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
}

function clearGameState() {
	// url = '/set_game_state/game%20on%2CThe%20show%20must%20go%20%2C1%2C1/' + KING_B0DH1_PA55W0RD
	url = '/set_game_state/Game On,The show must go on...,0,0/' + KING_B0DH1_PA55W0RD
	actionDesc = 'reset game state'
	takeControlAction(url, actionDesc)
}

function clearCoinScores() {
	url = '/reset_coin_scores/' + KING_B0DH1_PA55W0RD
	actionDesc = 'reset coin scores'
	takeControlAction(url, actionDesc)
}

function resetDB() {
	if(confirm('Really reset the DB?')) {
		url = '/clear_db/' + KING_B0DH1_PA55W0RD
		actionDesc = 'reset DB'
		takeControlAction(url, actionDesc)
	}
}
