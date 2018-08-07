<?php

require_once('common.php');

// Context Menu
$context_menu = file_get_contents(COMPONENTS . "/filemanager/context_menu.json");
$context_menu = json_decode($context_menu,true);

// Right Bar
$right_bar = file_get_contents(COMPONENTS . "/right_bar.json");
$right_bar = json_decode($right_bar,true);

// Read Components, Plugins, Themes
$components = Common::readDirectory(COMPONENTS);
$plugins = Common::readDirectory(PLUGINS);
$themes = Common::readDirectory(THEMES);

// Theme
$theme = THEME;
if(isset($_SESSION['theme'])) {
  $theme = $_SESSION['theme'];
}

?>
<!doctype html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?php i18n("SDN Login"); ?></title>
    <?php
    // Load System CSS Files
    $stylesheets = array("jquery.toastmessage.css","reset.css","fonts.css","screen.css");
   
    foreach($stylesheets as $sheet){
        if(file_exists(THEMES . "/". $theme . "/".$sheet)){
            echo('<link rel="stylesheet" href="themes/'.$theme.'/'.$sheet.'">');
        } else {
            echo('<link rel="stylesheet" href="themes/default/'.$sheet.'">');
        }
    }
    
    // Load Component CSS Files    
    foreach($components as $component){
        if(file_exists(THEMES . "/". $theme . "/" . $component . "/screen.css")){
            echo('<link rel="stylesheet" href="themes/'.$theme.'/'.$component.'/screen.css">');
        } else {
            if(file_exists("themes/default/" . $component . "/screen.css")){
                echo('<link rel="stylesheet" href="themes/default/'.$component.'/screen.css">');
            } else {
                if(file_exists(COMPONENTS . "/" . $component . "/screen.css")){
                    echo('<link rel="stylesheet" href="components/'.$component.'/screen.css">');
                }
            }
        }
    }
    
    // Load Plugin CSS Files    
    foreach($plugins as $plugin){
        if(file_exists(THEMES . "/". $theme . "/" . $plugin . "/screen.css")){
            echo('<link rel="stylesheet" href="themes/'.$theme.'/'.$plugin.'/screen.css">');
        } else {
            if(file_exists("themes/default/" . $plugin . "/screen.css")){
                echo('<link rel="stylesheet" href="themes/default/'.$plugin.'/screen.css">');
            } else {
                if(file_exists(PLUGINS . "/" . $plugin . "/screen.css")){
                    echo('<link rel="stylesheet" href="plugins/'.$plugin.'/screen.css">');
                }
            }
        }
    }
    ?> 
<link href="css/login.css" rel="stylesheet">
<link href="css/bootstrap.min.css" rel="stylesheet">
<link href="css/bootstrap.css" rel="stylesheet">
<link href="css/font-awesome.css" rel="stylesheet">
<link href="css/sdn.css" rel="stylesheet">
<link rel="icon" href="favicon.ico" type="image/x-icon" />
</head>
<body>
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
    <div id="message"></div>
