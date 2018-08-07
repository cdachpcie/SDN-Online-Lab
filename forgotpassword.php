<?php
//require_once('header.php');
require_once('header_u.php');
?>
<div class="col-lg-12">
	<div class="container">
		<form>
			<label><?php i18n("Username"); ?></label>
            <input type="text" class="form-control" name="username">
            <label><?php i18n("New Password"); ?></label>
            <input type="password" class="form-control" name="password1" >
            <label><?php i18n("Confirm Password"); ?></label>
            <input type="password" class="form-control" name="password2">
			<button class="btn-left"><?php i18n("Change Password") ?></button>
			<!--<button class="btn-right" onclick="codiad.modal.unload();return false;"><?php i18n("Cancel"); ?></button>-->
		</form>
	</div>
</div>


<script>
    
    $(document).ready(function(){
       $("form").submit(function(e) {
            e.preventDefault();
            
             var pass = true;
             var _this = this;
             
                var username = $('form input[name="username"]')
                    .val();   	
                var password1 = $('form input[name="password1"]')
                    .val();
                var password2 = $('form input[name="password2"]')
                    .val();
                // Check matching passwords
                if (password1 != password2) {
                    codiad.message.error(i18n('Passwords Do Not Match'));
                    pass = false;
                } 
                
                if (pass) {
                  var controller = 'components/user/controller.php';
                  var dialogue = '<?php echo BASE_URL; ?>/dialogue/user/dialogue.php';
                    $.post('components/user/controller.php' + '?action=password', {'username' : username , 'password' : password1 }, function(data) {
                        var createResponse = codiad.jsend.parse(data);
                        if (createResponse != 'error') {
                           var base_url = window.location.origin;
                            codiad.message.success(i18n('User Password Changed'));
                             window.location.href = base_url+"/login.php";
                            _this.list();
                        }
                    });
                }
        });
    });

</script>
 
 