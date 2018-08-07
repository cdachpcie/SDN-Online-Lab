 <script src="components/editor/ace-editor/ace.js"></script>
  <script>
    var i18n = (function(lang) {
        return function(word,args) {
            var x;
            var returnw = (word in lang) ? lang[word] : word;
            for(x in args){
                returnw=returnw.replace("%{"+x+"}%",args[x]);   
            }
            return returnw;
        }
    })(<?php echo json_encode($lang); ?>)
    </script>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    <script>!window.jQuery && document.write(unescape('%3Cscript src="js/jquery-1.7.2.min.js"%3E%3C/script%3E'));</script>
    <script src="js/jquery-ui-1.8.23.custom.min.js"></script>
    <script src="js/jquery.css3.min.js"></script>
    <script src="js/jquery.easing.js"></script>
    <script src="js/jquery.toastmessage.js"></script>
    <script src="js/amplify.min.js"></script>
    <script src="js/localstorage.js"></script>
    <script src="js/jquery.hoverIntent.min.js"></script>
    <script src="js/system.js"></script>
    <script src="js/sidebars.js"></script>
    <script src="js/modal.js"></script>
    <script src="js/message.js"></script>
    <script src="js/jsend.js"></script>
    <script src="js/instance.js?v=<?php echo time(); ?>"></script>

    <!-- COMPONENTS -->
    <?php

        require_once('common.php');


        $components = Common::readDirectory(COMPONENTS);
        $plugins = Common::readDirectory(PLUGINS);
        $themes = Common::readDirectory(THEMES);

        //////////////////////////////////////////////////////////////////
        // LOAD COMPONENTS
        //////////////////////////////////////////////////////////////////

        // JS
        foreach($components as $component){
            if(file_exists(COMPONENTS . "/" . $component . "/init.js")){
                echo('<script src="components/'.$component.'/init.js"></script>');
            }
        }
        
        foreach($plugins as $plugin){
            if(file_exists(PLUGINS . "/" . $plugin . "/init.js")){
                echo('<script src="plugins/'.$plugin.'/init.js"></script>');
            }
        }

    //}

    ?>
    
            <div class="footer-header" style="background-color: #fff">
                <div class="row">
                  <div class="col-md-6 col-sm-6 col-xs-12">
                    <div class="login-logo">
                      <img src="http://eindia.eletsonline.com/2017/wp-content/uploads/2016/09/Digital-India-300x200.png" alt="logo" class="img-responsive" style="max-width: 99px;">
                    </div>
                  </div>
                  <div class="col-md-6 col-sm-6 col-xs-12">
                    <div class="login-logo">
                      <img id="logo" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFpRSvbGIIjnkm6b_WXXQ79Ms9XnK6v8JhByhk1dcx24ULYFdwFQ"  style="max-width: 66px;margin-left:260px; ">
                    </div>
                  </div>
                </div>
              </div>
