var error

function writeError(){
	var errorMessage = document.getElementById("errorMessage");
	errorMessage.innerHTML = (error);
}
function prohibitSubmit(){
	var errorMessage = document.getElementById("errorMessage");
	var fakeButton = document.getElementById("fakeButton");
	var submit = document.getElementById("submit");
	fakeButton.style.display = "block";
	submit.style.display = "none";
}
function allowSubmit(){
	var errorMessage = document.getElementById("errorMessage");
	var fakeButton = document.getElementById("fakeButton");
	var submit = document.getElementById("submit");
	errorMessage.innerHTML = ("");
	fakeButton.style.display = "none";
	submit.style.display = "block";
}