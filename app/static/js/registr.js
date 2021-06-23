var username;
var password1;
var password2;

function checkData(event) {
	var errorMessage = document.getElementById("errorMessage");
	if (!username.value) {
		prohibitSubmit();
		error = "Необходимо ввести логин.";
		return;
	}
	if (!password1.value) {
		prohibitSubmit();
		error = "Необходимо ввести пароль.";
		return;
	}
	if (!password2.value) {
		prohibitSubmit();
		error = "Необходимо подтвердить пароль.";
		return;
	}
	if (password1.value != password2.value) {
		prohibitSubmit();
		error = "Пароли не совпадают.";
		return;
	}
	allowSubmit();
}

window.addEventListener("load", function() {
    username = document.getElementById("username");
    password1 = document.getElementById("password1");
    password2 = document.getElementById("password2");
    username.addEventListener("change", checkData);
    password1.addEventListener("change", checkData);
    password2.addEventListener("change", checkData);
	error = "Необходимо ввести логин.";
});