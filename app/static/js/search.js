var searchField;
var hints;
var res_json
var display = true;


function CreateRequest()
{
    var Request = false;
    if (window.XMLHttpRequest)
    {
        Request = new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        try
        {
             Request = new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch (CatchException)
        {
             Request = new ActiveXObject("Msxml2.XMLHTTP");
        }
    }
    if (!Request)
    {
        alert("Невозможно создать XMLHttpRequest");
    }
    return Request;
}

function past_hints(json){
    hints.innerHTML = '';
    hints.style.display = 'flex';
    for (var tag in json) {
        let a = document.createElement('a')
        a.href = `/tag_page/${json[tag].id}/`;
        a.innerHTML = '#' + json[tag].name;
        a.style.textTransform = 'capitalize';
        a.style.color = 'black';
        hints.append(a);
    }
}

function doRequest(event){
    var Request = CreateRequest();
    var r_method = "POST";
    var json = JSON.stringify(searchField.value);

    Request.open(r_method, r_path, true);

    Request.setRequestHeader("Content-Type","application/json; charset=utf-8");

    Request.addEventListener("readystatechange", () => {

        if(Request.readyState === 4 && Request.status === 200) {
            res_json = JSON.parse(Request.responseText);
            past_hints(res_json);
        }
    });
    Request.send(json);
}

function keyPress(e){
                var key, x = e || window.event; key = (x.keyCode || x.which);
                if(key <= 90 && key  >= 48){
                    doRequest();
                }
            }

window.addEventListener("load", function (){
    hints = document.getElementById('hints');
    searchField = document.getElementById('searchField');
    searchField.addEventListener('focus', function (){
        document.addEventListener('keyup', function (event){
            keyPress(event);
        });
    });
    searchField.addEventListener('blur', function (){
            function timer() {
                hints.style.display = 'none';
            }
            setTimeout(timer, 100);
    });
});