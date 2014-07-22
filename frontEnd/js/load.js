var canvas;
var context;
var HEIGHT=600, WIDTH=1024;
var dx=15,dy=15;
var x=50,y=50;
var runAnimation=true;

window.addEventListener('keydown',performKeyDownEvent,true);

function startView(){
	if(document.cookie.split('=')[1]){
		canvas=document.getElementById("myCanvas");
		context=canvas.getContext('2d');
		reDraw();
		draw();
	}
	else{alert("Very funny lah!!!");restartGame()};
}


function draw() {
	if (runAnimation){
		context.clearRect(0, 0, WIDTH, HEIGHT);
		context.fillStyle = "white";
		context.rect(0,0,WIDTH,HEIGHT);
// 		context.strokeStyle = "black";
		
		drawEach(document.cookie.split('=')[1].toUpperCase(),'white','black');
	}
}


function drawEach(name,colorFill, colorStroke){

	console.log(x,y);
	context.rect(x, y, Math.round(context.measureText(name).width)+10, 20);
	context.fillStyle = colorFill;
	context.fill();
	context.lineWidth = 7;
	context.strokeStyle = colorStroke;
	context.stroke();
	context.fillStyle='red';
	n=context.fillText(name, x+5, y+13);
	
	
}

function drawOthers(names){
// draw others as and when they join the game
	for (var i =0; i < names.length; i++){
		// draw the others
	}
}

function performKeyDownEvent(event){
	switch (event.keyCode) {
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
			if (x - dx > 0){
				x -= dx;
			}
		break;
		case 39:  /* Right arrow was pressed */
			if (x + dx < WIDTH){
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