function pushCoin(){
	$.getJSON('/game_state', function(data){
		game_state = data
		coins = game_state['coins']
		players = game_state['players']
		var locations= new Array();
		for (var i=0;i<18; i++){
			for (var j=0;j<37;j++){
				locations[i][j]=0;
			}
		}
		for (var coin in coins){
			locations[coin['location_x']['location_y']]=1
		}
		
		for (var player in players){
			locations[coin['location_x']['location_y']=1
		}
		var flag=0;
		while (flag==0){
			randomX=Math.Round(Math.random()*37)
			randomY=Math.Round(Math.random()*18)
			if (locations[randomX][randomY]==0){
				// do something to place coin
				
				//get control password
				password=window.location.href.split('control')[1].split['/'][1]
				console.log(password)
				pushCoinURL='/add_coin/'+ randomX + '/' + randomY + '/' + password
				$.getJSON(pushCoinURL,function(){
				});
		}
	});
}

function sleepforFiveSeconds(){
	setTimeout(pushCoin(),3000);
}