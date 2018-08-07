<?php 
require_once('header.php');
//print_r($_SESSION);
$link = $_SERVER['PHP_SELF'];
$link_array = explode('/',$link);
$page = end($link_array);
if(!isset($_SESSION['user'])){
$path = rtrim(str_replace($page, "", $_SERVER['SCRIPT_FILENAME']),"/");
$users = file_exists($path . "/data/users.php");
$projects = file_exists($path . "/data/projects.php");
$active = file_exists($path . "/data/active.php");
if(!$users && !$projects && !$active){
// Installer
require_once('components/install/view.php');
}else{
// Login form
?>
<style>
.logoblink{
    padding: 20px;
}
.message{
    text-align: center;
    margin-top: 19px;
    color: #009846;
    font-weight: bold;
    margin-left: 12px;
    font-size: 14px;
    line-height: 20px;
}
</style>
<body class="loginbg" style="overflow-y: auto;">
  <div class="container">
    <div class="row">
      <div class="login-area">
        <div class="bg-image">
          <div class="login-signup">
            <div class="container">
              <div class="login-header">
                <div class="row">
                  <div class="col-md-6 col-sm-6 col-xs-12">
                    <div class="login-logo">
                      <img src="images/logo.png" alt="logo" class="img-responsive">
                    </div>
                  </div>
                <!--  <div class="col-md-2 col-sm-2 col-xs-12 logoblink">
                         <img id="logo" height="50" width="50" />
                  </div>-->
                  <div class="col-md-6 col-sm-6 col-xs-12">
                    <div class="login-details">
                      <ul class="nav nav-tabs navbar-right">
                        <li>
                          <a data-toggle="tab" href="#register"> 
                            <i class="fa fa-user-plus" aria-hidden="true">
                            </i> Register
                          </a>
                        </li>
                        <li class="active">
                          <a data-toggle="tab" href="#login1">
                            <i class="fa fa-power-off" aria-hidden="true">
                            </i> Login
                          </a>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              <div class="tab-content">
                <div id="register" class="tab-pane">
                  <div class="login-inner">
                    <div class="title">
                      <h1>Welcome
                      </h1>
                    </div>
                    <div class="login-form">
                      <form id=¨createForm¨>
                        <div class="form-details">
                          <label class="user">
                            <!--<input type="hidden" name="action" value="create">-->
                            <input type="text" name="username" placeholder="Full Name" id="username" required>
                          </label>
                          <label class="mail">
                            <input type="email" name="email" placeholder="Email Address" id="email" required>
                          </label>
                          <label class="pass">
                            <input type="password" name="password1" placeholder="Password" id="password" required>
                          </label>
                          <label class="pass">
                            <input type="password" name="password2" placeholder="Confirm Password" id="password" required>
                          </label>
                          <label class="organization">
                            <input type="text" name="organization" placeholder="Enter Organization Name" id="organization" required>
                          </label>
                          <label class="city">
                            <input type="text" name="city" placeholder="Enter City" id="city" required>
                          </label>
                        </div>
                        <a onclick=codiad.user.createNew();> 
                            <button  class="form-btn">
                      <?php i18n("Create"); ?>
                    </button>
                        </a>
                      </form>
                    </div>
                  </div>
                </div>
                <div id="login1" class="tab-pane fade in active">
                  <div class="login-inner">
                    <div class="title">
                      <h1>Welcome 
                      </h1>
                     
                <?php
                    if (isset($_SESSION['message']) && $_SESSION['message'] != '') {   ?>
                        <div class="message"><?php echo $_SESSION['message'] ?></div>
                <?php
                        unset($_SESSION['message']);
                    }
                ?>
                  
                    </div>
                    <div class="login-form">
                      <!--  <form id="login" method="post" style="position: fixed; width: 350px; top: 30%; left: 50%; margin-left: -175px; padding: 35px;"> -->
                      <form id="login" method="post">
                        <div class="form-details">
                          <label class="user">
                            <input type="text" name="username" autofocus="autofocus" autocomplete="off" placeholder="Username" id="username" required>
                          </label>
                          <label class="pass">
                            <input type="password" name="password" placeholder="Password" id="password" required>
                          </label>
                          <div class="language-selector">
                            <label>
                              <span class="icon-picture login-icon">
                              </span> 
                              <?php i18n("Theme"); ?>
                            </label>
                            <select name="theme" id="theme">
                              <option value="default">
                                <?php i18n("Default"); ?>
                              </option>
                              <?php
                                include 'languages/code.php';
                                foreach($themes as $theme): 
                                if(file_exists(THEMES."/" . $theme . "/theme.json")) {
                                $data = file_get_contents(THEMES."/" . $theme . "/theme.json");
                                $data = json_decode($data,true);
                               ?>
                              <option value="<?php echo $theme; ?>" 
                                      <?php if($theme == THEME) { echo "selected"; } ?>>
                              <?php if($data[0]['name'] != '') { echo $data[0]['name']; } else { echo $theme; } ?>
                              </option>
                            <?php } endforeach; ?>
                            </select>
                          <label>
                            <span class="icon-language login-icon">
                            </span> 
                            <?php i18n("Language"); ?>
                          </label>
                          <select name="language" id="language">
                            <?php
                                include 'languages/code.php';
                                foreach(glob("languages/*.php") as $filename): 
                                $lang_code = str_replace(array("languages/", ".php"), "", $filename);
                                if(!isset($languages[$lang_code])) continue;
                                $lang_disp = ucfirst(strtolower($languages[$lang_code]));
                            ?>
                            <option value="<?php echo $lang_code; ?>" 
                                    <?php if ($lang_code == "en"){echo "selected";}?>>
                            <?php echo $lang_disp; ?>
                            </option>
                          <?php endforeach; ?>
                          </select>
                        </div>
                    </div>
                    <button  class="form-btn">
                      <?php i18n("Login"); ?>
                    </button><br>
                    <a href="forgotpassword.php" class="">Forgot Password ?</a>
                    <!--  <a class="show-language-selector"><?php i18n("More"); ?></a> -->
                    </form>
                    </div>
                  </div>
                </div>
              </div>
                  <script src="components/user/init.js"></script>
                  <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
                  <script src="js/jquery.min.js"> </script>
                  <!-- Include all compiled plugins (below), or include individual files as needed -->
                  <script src="js/bootstrap.min.js"></script>
                  <?php  } 
}
else
{
$variable = "index.php";
header('Location: ' .$variable);
}?>



<script>

    $(document).ready(function(){
       $("form").submit(function(e) {
            e.preventDefault();
            
             var pass = true;
             var _this = this;
             
                var username = $('#register form input[name="username"]')
                    .val();
                var email = $('#register form input[name="email"]')
                    .val();    
                var password1 = $('#register form input[name="password1"]')
                    .val();
                var password2 = $('#register form input[name="password2"]')
                    .val();
                var organization = $('#register form input[name="organization"]')
                    .val();
                var city = $('#register form input[name="city"]')
                    .val();
                
                // Check matching passwords
                if (password1 != password2) {
                    codiad.message.error(i18n('Passwords Do Not Match'));
                    pass = false;
                } 
                // Check no spaces in username
                if (!/^[a-z0-9]+$/i.test(username) || username.length===0) {
                    codiad.message.error(i18n('Username Must Be Alphanumeric String'));
                    pass = false;
                }
                
                if (pass) {
                  var controller = 'components/user/controller.php';
                  var dialogue = '<?php echo BASE_URL; ?>/dialogue/user/dialogue.php';
                    $.post('components/user/controller.php' + '?action=create', {'username' : username , 'email' : email , 'password' : password1 ,'organization' : organization, 'city' : city,'status' : '0' }, function(data) {
                      alert(data);
                    // alert(dialogue);
                        var createResponse = codiad.jsend.parse(data);
                        var usernames = email+'&'+username;
                        if (createResponse != 'error') {
                           var base_url = window.location.origin;
                            codiad.message.success(i18n('User Account Created'));
                             window.location.href = base_url+"/send-email-php/mail.php?email="+usernames;
                            _this.list();
                        }
                    });
                }
        });
    });

</script>
<?php 
require_once('footerlogin.php');
?>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
        