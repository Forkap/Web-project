var preview;
var updatePreview;
var filename;
var file;

function checkData(event){
	var errorMessage = document.getElementById("errorMessage");
	if (!filename.value) {
		prohibitSubmit();
		error = "Необходимо ввести название файла.";
		return;
	}
	if (!file.files[0]) {
		prohibitSubmit();
		error = "Необходимо выбрать фаил.";
		return;
	}
	allowSubmit();
}

window.addEventListener("load", function() {
	preview = document.getElementById('preview');
	preview.style.display = "none";
	updatePreview = function(event) {
			preview.src = URL.createObjectURL(event.target.files[0]);
			preview.style.display = "block";
			preview.onload = function() {
				URL.revokeObjectURL(preview.src);
			}
		};
    filename = document.getElementById("filename");
    file = document.getElementById("file");
    filename.addEventListener("change", checkData);
    file.addEventListener("change", checkData);
	error = "Необходимо ввести название файла.";
});