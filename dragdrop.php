<html>
<head>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

<!-- jQuery library -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

<!-- Latest compiled JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> 
<style>
#div1 {
    width: 750px;
    height: 350px;
   /* padding: 10px;*/
    border: 1px solid #aaaaaa;
}
.header{
    background: #D9D9D9; 
}
.left-side{
    background: #D9D9D9;
    margin-left: -15px;
    width: 65%;
}
.logo-adjust{
    margin: 10px;
}
#mydiv1{
    position: absolute;
}
.drag1 {
    cursor: move;
    position: relative;
}
</style>
<script>
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);

}

var n = 500;
var dragok = false;
var y,x,d,dy,dx;

function move(e){
if (!e) e = window.event;
 if (dragok){
  d.style.left = dx + e.clientX - x + "px";
  d.style.top  = dy + e.clientY - y + "px";
  return false;
 }
}

function drop(ev) {
   
     
     ev.preventDefault();  
    var data = ev.dataTransfer.getData("text");
    var nodeCopy = document.getElementById(data).cloneNode(true);
   // var test=0;
   // test++;
   
    
   // nodeCopy.id = "newId";
    nodeCopy.setAttribute("class", "drag1");
    nodeCopy.setAttribute("draggable", "false");
    
    var temp = (typeof ev.target != "undefined")?ev.target:e.srcElement;
      if (temp.tagName != "HTML"|"BODY" && temp.className != "drag1"){
         temp = (typeof temp.parentNode != "undefined")?temp.parentNode:temp.parentElement;
         }
     //   if (temp.className == "drag1"){
         //   alert(temp);

      //  if (window.opera){
       //   document.getElementById("newId").focus();
       //  }
         dragok = true;
         temp.style.zIndex = n++;
         d = temp;
         dx = parseInt(temp.style.left+0);
         dy = parseInt(temp.style.top+0);
         x = ev.clientX;
         y = ev.clientY;
         alert(x);
         alert(y);
         document.onmousemove = move;
      //   return false;
      //   }
      
    nodeCopy.id =dx; /* We cannot use the same ID */
    var newNodeId = nodeCopy.id;
  //  alert(newNodeId);
     ev.target.appendChild(nodeCopy);
    document.getElementById(newNodeId).style.position = "relative";
    document.getElementById(newNodeId).style.left = x;
    document.getElementById(newNodeId).style.top = y;
   
   // alert(temp);
   // dragElement(document.getElementById(("div1")));
   // dragElement(document.getElementsByClassName("drag1"));
   // ev.target.appendChild(document.getElementById(data));
}


</script>
</head>
<body>
        <div class="col-lg-12">
            <div class="header"><button>File</button><button>Edit</button><button>Run</button><button>Help</button></div>
            <div id="mydiv1">
                <div class="col-lg-2">
                    <div class="left-side">
                        <div draggable="true" ondragstart="drag(event)">
                            <img class="logo-adjust" id="drag1" src="images/switch.png"  width="56" height="69">
                        </div>
                        <div draggable="true" ondragstart="drag(event)">
                            <img class="logo-adjust" id="drag2" src="images/controller.png" width="56" height="69">
                        </div>
                        <div draggable="true" ondragstart="drag(event)">
                            <img class="logo-adjust" id="drag3" src="images/networks.png" width="56" height="69">
                        </div>
                        <div draggable="true" ondragstart="drag(event)">
                            <img class="logo-adjust" id="drag4" src="images/sdnc.png" width="56" height="150">
                        </div>
                    </div>
                </div>
                <div class="col-lg-10">
                    <div class="right-side">
                        <div id="div1" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
                    </div>
                </div>
             </div>
        </div>

</body>
</html>

<!--<!DOCTYPE html>
<html>
<style>
#mydiv {
    position: absolute;
    z-index: 9;
    background-color: #f1f1f1;
    text-align: center;
    border: 1px solid #d3d3d3;
}

#mydivheader {
    padding: 10px;
    cursor: move;
    z-index: 10;
    background-color: #2196F3;
    color: #fff;
}
</style>
<body>

<h1>Draggable DIV Element</h1>

<p>Click and hold the mouse button down while moving the DIV element</p>

<div id="mydiv" class="drag1111">
  <div id="mydivheader">Click here to move</div>
  <p>Move</p>
  <p>this</p>
  <p>DIV</p>
</div>
-->
<script>
//Make the DIV element draggagle:
//dragElement(document.getElementById(("mydiv")));
//dragElement(document.getElementsByClassName("drag1111"));
//function dragElement(elmnt) {
//  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
//  //alert(pos1);
//  if (document.getElementById(elmnt.id + "header")) {
//    /* if present, the header is where you move the DIV from:*/
//    document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
//  } else {
//   //  alert(elmnt);
//    /* otherwise, move the DIV from anywhere inside the DIV:*/
//  //  elmnt.onmousedown = dragMouseDown;
//  
//  
//     pos3 = e.clientX;
//    pos4 = e.clientY;
//    //alert(clientX);
//    document.onmouseup = closeDragElement;
//    // call a function whenever the cursor moves:
//    document.onmousemove = elementDrag;
//    
//  }
//
//  function dragMouseDown(e) {
//  //  alert(clientX);
//   //  alert("header");
//   // e = e || window.event;
//   e = e.preventDefault();
//    // get the mouse cursor position at startup:
//    pos3 = e.clientX;
//    pos4 = e.clientY;
//    //alert(clientX);
//    document.onmouseup = closeDragElement;
//    // call a function whenever the cursor moves:
//    document.onmousemove = elementDrag;
//  }
//
//  function elementDrag(e) {
//   //  alert("header1");
//   // e = e || window.event;
//     e = e.preventDefault();
//    // calculate the new cursor position:
//    pos1 = pos3 - e.clientX;
//    pos2 = pos4 - e.clientY;
//    pos3 = e.clientX;
//    pos4 = e.clientY;
//    // set the element's new position:
//    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
//    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
//  }
//
//  function closeDragElement() {
//    /* stop moving when mouse button is released:*/
//    document.onmouseup = null;
//    document.onmousemove = null;
//  }
//}
</script>
<!--
</body>
</html>-->
<!--

<style type="text/css">
.dragclass{
position : relative;
cursor : move;
}
</style>

<script type="text/javascript" src="dragdrop.js"></script>



 <p class="dragclass" style="color:red">
 Blah blah 
 </p>


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>

<title>Drag and Drop</title>
<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">
<meta http-equiv="content-script-type" content="text/javascript">
<meta http-equiv="content-style-type" content="text/css">


<style type="text/css">
.dragclass{
position : relative;
cursor : move;
}
</style>


<script type="text/javascript">
//Drag and Drop script - http://www.btinternet.com/~kurt.grigg/javascript

if  (document.getElementById){

(function(){

//Stop Opera selecting anything whilst dragging.
if (window.opera){
document.write("<input type='hidden' id='Q' value=' '>");
}

var n = 500;
var dragok = false;
var y,x,d,dy,dx;

function move(e){
if (!e) e = window.event;
 if (dragok){
  d.style.left = dx + e.clientX - x + "px";
  d.style.top  = dy + e.clientY - y + "px";
  return false;
 }
}

function down(e){
if (!e) e = window.event;
var temp = (typeof e.target != "undefined")?e.target:e.srcElement;
if (temp.tagName != "HTML"|"BODY" && temp.className != "dragclass"){
 temp = (typeof temp.parentNode != "undefined")?temp.parentNode:temp.parentElement;
 }
if (temp.className == "dragclass"){
 if (window.opera){
  document.getElementById("Q").focus();
 }
 dragok = true;
 temp.style.zIndex = n++;
 d = temp;
 dx = parseInt(temp.style.left+0);
 dy = parseInt(temp.style.top+0);
 x = e.clientX;
 y = e.clientY;
 document.onmousemove = move;
 return false;
 }
}

function up(){
dragok = false;
document.onmousemove = null;
}

document.onmousedown = down;
document.onmouseup = up;

})();
}//End.
</script>


</head>
<body>






<p class="dragclass" style="top:0px;left:0px;width:200px;text-align:center;background-color:#ff0000;color:#ffffff">
P tag 
</p>


<div class="dragclass" style="height:20px;width:150px;top:0px;left:0px;background-color:#ff0000;color:#ffffff">
Div: Relative position
</div>

<p>.</p>



<img src="http://www.java2s.com/style/logo.png" class="dragclass" style="top:0px;left:0px;height:100px;width:150px;padding:0px"/>
<p>.<p>


<b class="dragclass" style="top:0px;left:0px;background-color:#ff0000;color:#ffffff">
B tag
</b>



<img src="http://www.java2s.com/style/logoRed.png" class="dragclass" style="position:absolute;top:400px;left:200px;height:105px;width:150px;padding:0px"/>

<div id="test" class="dragclass" style="position:absolute;top:330px;left:160px;height:20px;width:150px;background-color:#ff0000;color:#ffffff">
Div: Absolute position
</div>


</body>
</html>
-->