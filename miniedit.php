 
<?php

  //require_once('common.php');
    
    //////////////////////////////////////////////////////////////////
    // Verify Session or Key
    //////////////////////////////////////////////////////////////////

require_once('header_new.php');
checkSession(); 
//$_SESSION['lang'] ='en';
//echo '<pre>';print_r($_SESSION);die;

   $projects_assigned = false;
            if(file_exists(BASE_PATH . "/data/" . $_SESSION['user'] . '_acl.php')){
                $projects_assigned = getJSON($_SESSION['user'] . '_acl.php');
            }
            
            ?>
            
            	<style>
	
.modal-content-set {
  position: relative;
  background-color: #fff;
  -webkit-background-clip: padding-box;
          background-clip: padding-box;
  border: 1px solid #999;
  border: 1px solid rgba(0, 0, 0, .2);
  border-radius: 6px;
  outline: 0;
  -webkit-box-shadow: 0 3px 9px rgba(0, 0, 0, .5);
          box-shadow: 0 3px 9px rgba(0, 0, 0, .5);
}

@media (min-width: 768px) {
  .modal-dialog-set {
    width: 800px;
    margin: 30px auto;
  }
  .modal-content-set {
    -webkit-box-shadow: 0 5px 15px rgba(0, 0, 0, .5);
            box-shadow: 0 5px 15px rgba(0, 0, 0, .5);
  }
	
.modal-body-set {
  position: relative;
  padding: 15px;
  min-height:300px;
  overflow:auto;
}	


.tabs-left > .nav-tabs {
    float: left;
    margin-right: 19px;
    border: none;
}

.tabs-below > .nav-tabs, .tabs-right > .nav-tabs, .tabs-left > .nav-tabs {
    border-bottom: 0;
}

.tabs-left > .nav-tabs > li, .tabs-right > .nav-tabs > li {
    float: none;
}

.tabs-left > .nav-tabs > li > a {
    margin-right: -1px;
    -webkit-border-radius: 4px 0 0 4px;
    -moz-border-radius: 4px 0 0 4px;
    border-radius: 4px 0 0 4px;
}
.tabs-left > .nav-tabs > li > a, .tabs-right > .nav-tabs > li > a {
    min-width: 74px;
    margin-right: 0;
    margin-bottom: 3px;
    background-color: #6ac0de;
    border-radius:0px;
    color: white;
}

.tabs-left > .nav-tabs .active > a, .tabs-left > .nav-tabs .active > a:hover, .tabs-left > .nav-tabs .active > a:focus {
    border-color: #ddd transparent #ddd #ddd;
	    background-color: #f8f8f8;
color: dimgrey;
border:none;
}

.left-tab-process .tab-content{
	background-color:#f8f8f8;
	   margin-left: 115px;
		overflow:x scroll;}

.tab-content > .active, .pill-content > .active {
    display: block;
}

.book-process-ltab{
	max-width:135px;}
	
.left-tab-process .tab-pane{
    padding: 11px 32px;
    min-height: 300px;
}

.left-tab-process h4{
	color:#536779;}
	
.term-fa{
margin-right: 7px;
    font-size: 11px;
    margin-left: -18px;
    color: #2EA72F;}
    
.tac-content{
    background-color:#ccc;}

	</style>
				<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

<!-- jQuery library -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

<!-- Latest compiled JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script type="text/javascript" src="CustomDialog/wz_jsgraphics.js"></script>
<style>
#div1 {
    width: 740px;
    height: 450px;
    /*padding: 10px;*/
    /*border: 1px solid #aaaaaa;*/
}
.header{
    background: #D9D9D9;
    border-bottom: 1px solid grey;
    padding: 5px;
}
.left-side{
    background: #D9D9D9;
    margin-left: -15px;
    width: 195%;
}
.logo-adjust{
    margin: 10px;
}
#mydiv1{
    position: absolute;
}
.drag1 {
    position:absolute;  
}
.header span {
    font-size: 14px;
    padding: 10px;
}
</style>
<script>
    
    var mouseDown = false;
	//var clonedElm = null;
	var xOffset = 0, yOffset = 0;

    

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);  
}



function drop(ev) {
    var pos1,pos2,pos3,pos4;
    ev.preventDefault();  
    var data = ev.dataTransfer.getData("text");
    var nodeCopy = document.getElementById(data).cloneNode(true);
    nodeCopy.setAttribute("class", "drag1");
    nodeCopy.setAttribute("ondragstart", "onMouseMove(event);")
    nodeCopy.setAttribute("ondragover", "onMouseUp(event);")
    
    
    var div=document.getElementById("div1");
    var rect = div.getBoundingClientRect();
     
     var divposx = rect.left;/* div position pixels to calculate relative distance*/
     var divposy = rect.top;
    
    
    var posx = ev.clientX;
    var posy = ev.clientY;
    
    div.appendChild(nodeCopy);/* appended child dynamically*/
    nodeCopy.style.left = posx-divposx-(56/2);/* width/2 and height/2 to arrange in center */
    nodeCopy.style.top = posy-divposy-(70/2);
   
    }
    
 /* to see pixels of div and manipulate*/
  function onrandomclick(e){
      e= e || window.event;
      console.log(e.clientX+"\t" +e.clientY);
  }
  
  function onMouseMove (ev)
	{
      //  alert("hii");
        alert(nodeCopy);
		//if (clonedElm == null)
		//	return;

		$(nodeCopy).offset({
        	left: ev.pageX + xOffset,
        	top: ev.pageY + yOffset
        });

        return false;
	}
    
    function onMouseUp (ev)
	{
		//check if object is dropped on droppable element
		var droppableElements = $(".rk_droppable");

		if (droppableElements.length == 0)
		{
			cancelDrop(e);
		}
		else
		{
			var droppableElm = null;
			for (var i = droppableElements.length-1; i >= 0; i--)
			{
				if (isLocationInElement(droppableElements[i], ev.pageX, ev.pageY))
				{
					droppableElm = droppableElements[i];
                    alert(droppableElm);
					break;
				}
			}

			if (droppableElm == null)
				cancelDrop(ev);
			else
				drop (ev);
		}

		mouseDown = false;
		//nodeCopy = null;
		xOffset = 0;
		yOffset = 0;
    }
    
    function cancelDrop (event)
	{
		if (nodeCopy == null)
			return;
		if (!$(nodeCopy).hasClass("rk_clonable"))
		{
			$(nodeCopy).remove();
		}
		nodeCopy = null;
	}
    
    function isLocationInElement (element, x, y)
	{
		var elmOffset = $(element).offset();
		if (x >= elmOffset.left && x <= (elmOffset.left + $(element).width()) &&
			y >= elmOffset.top && y <= (elmOffset.top + $(element).height()))
			return true;
		return false;
	}


    
  document.onmouseup = onrandomclick;
 // document.mousemove = onMouseMove;

 
 function drawlines(ev){      
        var x0,y0,x1,y1,flag=0;
        
        
        function mouseDown(ev){
                if(flag == 0)
                {
                        var result_x2 = document.getElementById("x2_point");
                        var result_y2 = document.getElementById("y2_point");
                      //  alert(result_y2);
                        x0 = ev.clientX;
                        y0 = ev.clientY;
                        flag=1;
                }
                else
                {
                        var result_x1 = document.getElementById("x1_point");
                        var result_y1 = document.getElementById("y1_point");
                     //   alert(result_y2);
                        x1 = ev.clientX;
                        y1 = ev.clientY;
                        var jg = new jsGraphics("div1");    
                        jg.setColor("red");
                        jg.drawLine(x0, y0, x1, y1);
                        jg.paint();
                        flag=0;
                }
        }
        
        document.onmousedown = mouseDown;
  }    
</script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]> -->
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
      
<div class="container-fluid" style="width: 100%;position: absolute;">
    <div class="row">
        <!--main panal Start-->
		  <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
            <div class="header"><span>File</span><span>Edit</span><span>Run</span><span>Help</span></div>
            <div id="mydiv1">
                <div class="col-xs-1 col-sm-1 col-md-1 col-lg-1">
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
                            <img class="logo-adjust" id="drag4" src="images/rcontroller.png" width="56" height="69">
                        </div>
                         <div>
                            <img onclick="drawlines(event)"; class="logo-adjust" src="images/line.png" width="56" height="69">
                        </div>
                        <div draggable="true" ondragstart="drag(event)">
                            <img class="logo-adjust" id="drag5" src="images/controller (2).png" width="56" height="69">
                        </div>
                    </div>
                </div>
				
				<h2 id="x1_point"></h2>
				<h2 id="y1_point"></h2>
				<h2 id="x2_point"></h2>
				<h2 id="y2_point"></h2>
                <div class="col-xs-11 col-sm-11 col-md-11 col-lg-11">
                    <div class="right-side">
                        <div id="div1" class="rk_droppable" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
                    </div>
                </div>
             </div>
        </div>
	</div>
    </div>



<script src="js/custom.js"></script>
    
              <?php 
require_once('footer.php');
?>