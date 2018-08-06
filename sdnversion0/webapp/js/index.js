function login() {
    alert("sending");
    var xhr = new XMLHttpRequest();
    var url = "http://10.208.15.81:9000/api/auth";
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.addEventListener("readystatechange", processRequest, false);
    xhr.onreadystatechange = processRequest;
    
    var data = JSON.stringify({ "Username": "admin", "Password": "admin" });
    document.getElementById("id1").innerHTML += data;
    alert("sending");
    xhr.send(data);
   // var div = document.getElementById('id1');
//window.location.assign("dashboard.html")
}
function processRequest(e) {
    alert("inside func");
    if (xhr.readyState == 4 && xhr.status == 200) {
        var json = JSON.parse(xhr.responseText);
        alert(responseText.ip);
        document.getElementById("id1").innerHTML = json;
        window.location.assign("dashboard.html")
    }
}
