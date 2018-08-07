/*function login21() {
    alert("hi");
       document.getElementById("id1").innerHTML += "Hello";
}

function login2() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        alert(xhr.status);
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("id1").innerHTML = this.responseText;
    }
  };
    //xhr.onreadystatechange = processRequest;
    var url = "https://10.208.15.81:9000/api/auth";
    //alert(url);
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.setRequestHeader("Access-Control-Request-Methods","POST");
    xhr.setRequestHeader("Access-Control-Allow-Origin","*");
  //  alert(xhr.onreadystatechange);
    var dataRaw = {
"Username":"admin",
"Password":"prashant"
};
    var data = JSON.stringify(dataRaw);
    document.getElementById("id1").innerHTML += data;
   // alert(data);
    //alert("sending");
    xhr.send(data);
   // var div = document.getElementById('id1');
//window.location.assign("dashboard.html")

function processRequest(e) {
     alert(xhr.status);
  //  alert("inside func");
    if (xhr.readyState == 4 && xhr.status == 200) {
        alert(xhr.responseText);
        var json = JSON.parse(xhr.responseText);
        alert(xhr.responseText);
        document.getElementById("id1").innerHTML = json;
        window.location.assign("dashboard.html");
    }
}
}
function login() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  alert(this.status);
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("id1").innerHTML = this.responseText;
    }
  };
  xhttp.open("POST", "https://www.bearcreeksmokehouse.com", false);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.setRequestHeader("Access-Control-Allow-Origin","*");
  xhttp.send("fname=Henry&lname=Ford");
}
*/
function login() {

    var dataRaw = {
        "Username": "admin",
        "Password": "prashant"
    };
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://10.208.15.81:9000/api/auth", true);
    var data = JSON.stringify(dataRaw);
    xhr.onload = function() {
        console.log(xhr.responseText);
        alert(xhr.responseText);
    };
    xhr.send(data);

}