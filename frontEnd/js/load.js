var canvas;
var context;
var HEIGHT=600, WIDTH=900;
var dx=60,dy=30;
var x=200,y=60;
var runAnimation=true;
var name=document.cookie.split('=')[1].toUpperCase();
window.addEventListener('keydown',performKeyDownEvent,true);

function startView(){
	if(document.cookie.split('=')[1]){
		canvas=document.getElementById("myCanvas");
		context=canvas.getContext('2d');
		draw();
		reDraw();
	}
	else{alert("Very funny lah!");restartGame()};
}


function draw() {
	if (runAnimation){
		context.beginPath();
		context.clearRect(0, 0, WIDTH, HEIGHT);
		
		// draw random blocks
		context.arc(WIDTH/2 - 60, HEIGHT/2-90, 50,0,2*Math.PI);
		context.closePath();
		context.beginPath();
		context.arc(WIDTH/2 - 60, HEIGHT/2, 50,0,2*Math.PI);
		context.fillStyle = '#00FFFF';
		context.fill();
		context.lineWidth = 7;
		context.strokeStyle = 'black';
		context.stroke();
		context.closePath();
		// Draw players
		drawEach('blue'); // for _self_
		//drawOthers(); 
	}
}


function drawEach(colorStroke){

// 	console.log(x,y);
	context.beginPath();
// 	context.rect(x, y, Math.round(context.measureText(name).width)+10, 25);
	context.arc(x,y,context.measureText(name).width/2+10,0,2*Math.PI);
	context.fillStyle = '#FFFFFF';
	context.fill();
	context.lineWidth = 3;
	context.strokeStyle = colorStroke;
	context.stroke();
	context.closePath();
	context.beginPath();
	if (document.cookie.split('=')[1].toUpperCase()!=name){
		context.font="17px Serif";
		context.fillStyle='#000000';
	}
	else{
		context.font="20px Serif";
		context.fillStyle='#FF0000';
	}
	context.fillText(name, x-Math.round(context.measureText(name).width/2), y+5);
	context.closePath();
	
}

function drawOthers(names){
// draw others as and when they join the game
	for (var i =0; i < names.length; i++){
		// draw the others
		// drawEach(names[i], 'white', 'black');
	}
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