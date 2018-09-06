<html>
<style>
body {font-family: Arial, Helvetica, sans-serif;
background-image: linear-gradient( rgba(0, 0, 0, 0.5) 100%, rgba(0, 0, 0, 0.5)100%),url(https://images.idgesg.net/images/article/2017/09/networking-100735059-large.jpg);}
* {box-sizing: border-box;}

/* Button used to open the contact form - fixed at the bottom of the page */
.form-popup {
margin-top: 25px;
}

/* Add styles to the form container */
.form-container {
  max-width: 100%;
  padding: 30px;
  background-color: #05181C;
}

/* Full-width input fields */
.form-container input[type=text], select, .form-container input[type=select] {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  border: none;
  background: #f1f1f1;
}

/* When the inputs get focus, do something */
.form-container input[type=text]:focus, select, .form-container input[type=password]:focus {
  background-color: #ddd;
  outline: none;
}

/* Set a style for the submit/login button */
.form-container .btn {
  background-color: #337ab7;
  color: white;
  padding: 16px 20px;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-bottom:10px;
  opacity: 0.8;
}

/* Add a red background color to the cancel button */
.form-container .cancel {
  background-color: red;
}

/* Add some hover effects to buttons */
.form-container .btn:hover, .open-button:hover {
  opacity: 1;
}
b{
    color: white;
}
.selectBox { margin-left:0px; margin-bottom: 45px; background-color: white;}
</style>
<head>
<!-- Latest compiled and minified CSS -->

<!-- jQuery library -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<body>
<div class="col-lg-12">
    <div class="container">      
        <div class="form-popup" id="myForm">
          <form action="/webservice.php" method="POST" class="form-container">
            <!--<center><h1 style="color: white; margin-top: 0px;"><b>NETWORK EMULATOR</b></h1></center>-->
            
            <div class="row">
                <div class="col-sm-6">
                    <label for="email"><b>No of Switches</b></label>
                    <input type="text" placeholder="Enter No Switches" name="switches" required></div>
                <div class="col-sm-6">
                    <label for="email"><b>No of Hosts</b></label>
                    <input type="text" placeholder="Enter No Hosts" name="hosts" required>
                </div>
                 <div class="col-sm-6">
                    <label for="Controller"><b>Controller</b></label>
                    <select class="selectBox" name="controller" required>
                           <option value="pox">POX</option>
                           <option value="odl" disabled>ODL</option>
                    </select>
                 </div>
                <div class="col-sm-6">
                    <label for="Topology"><b>Topology</b></label>
                    <select class="selectBox" name="topology" required>
                        <option value="single">Single</option>
                        <option value="multiple" disabled>Multiple</option>
                    </select>
                </div>
            </div>
            <button type="submit" class="btn">Submit</button>
            <!--<button type="button" class="btn cancel" onclick="closeForm()">Cancel</button>-->
          </form>
        </div>
    </div>
</div>    

</div>
</div>   
</body>
</head>
</html>