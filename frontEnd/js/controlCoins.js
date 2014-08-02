// /set_game_state/game%20stop%2C"STOOOOOOOOP"%2C1%2C1/
// /set_game_state/

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
			$.getJSON(pushCoinURL);		
		}
		console.log(randomX,randomY);
		//sleepforSomeSeconds();
	});
	setTimeout(pushCoin, getNextInterarrivalTime());
	
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
