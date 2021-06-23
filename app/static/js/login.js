var username;
var password;
var fakeButton;

function checkData(event) {
	if (!username.value) {
		prohibitSubmit();
		error = "Необходимо ввести логин";
		return;
	}
	if (!password.value) {
		prohibitSubmit();
		error = "Необходимо ввести пароль";
		return;
	}
	allowSubmit();
}

window.addEventListener("load", function() {
    username = document.getElementById("username");
    password = document.getElementById("password");
    username.addEventListener("change", checkData);
    password.addEventListener("change", checkData);
	error = "Необходимо ввести логин";
});