var preview;
var updatePreview;

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

});