<?php
//require_once('header.php');
require_once('header_new.php');
?>
<body>
  
    <?php
//print_r($_SESSION);die;
    //////////////////////////////////////////////////////////////////
    // NOT LOGGED IN
    //////////////////////////////////////////////////////////////////

    if(!isset($_SESSION['user'])){
  ?>
  <script>
    
    var base_url = window.location.origin;
    window.location.href = base_url+"/login.php";
  
  </script>
  <?php 
    //////////////////////////////////////////////////////////////////
    // AUTHENTICATED
    //////////////////////////////////////////////////////////////////

    }else{

    ?>

    <div id="workspace">
        <div id="sb-left" class="sidebar left-menu">
            <div class="menu-tools-bg">				
                <div id="sb-left-title" class=¨left-menu-title¨>
                    <a id="lock-left-sidebar" class="icon-lock icon"></a>
                    <?php if (!common::isWINOS()) { ?>
                    <a id="finder-quick" class="icon icon-archive"></a>
                    <a id="tree-search" class="icon-search icon"></a>
                    <h2 id="finder-label"> <?php i18n("Explore"); ?> </h2>
                    <div id="finder-wrapper">
                       <a id="finder-options" class="icon icon-cog"></a>
                       <div id="finder-inner-wrapper">
                            <input type="text" id="finder"></input>
                       </div>
                       <ul id="finder-options-menu" class="options-menu">
                          <li class="chosen"><a data-option="left_prefix"><?php i18n("Prefix"); ?></a></li>
                          <li><a data-option="substring"><?php i18n("Substring"); ?></a></li>
                          <li><a data-option="regexp"><?php i18n("Regular expression"); ?></a></li>
                          <li><a data-action="search"><?php i18n("Search File Contents"); ?></a></li>
                       </ul>
                    </div>
                    <?php } ?>
                </div>

            <div class="sb-left-content left-menu-tool">
                <div id="context-menu" data-path="" data-type="">

                    <?php

                        ////////////////////////////////////////////////////////////
                        // Load Context Menu
                        ////////////////////////////////////////////////////////////

                        foreach($context_menu as $menu_item=>$data){
                            
                           // print_r($context_menu);

                            if($data['title']=='Break'){
                                echo('<hr class="'.$data['applies-to'].'">');
                            } else{
                                echo('<a class="'.$data['applies-to'].'" onclick="'.$data['onclick'].'"><span class="'.$data['icon'].'"></span>'.get_i18n($data['title']).'</a>');
                            }

                        }
                        
                        foreach ($plugins as $plugin){
                            if(file_exists(PLUGINS . "/" . $plugin . "/plugin.json")) {
                                $pdata = file_get_contents(PLUGINS . "/" . $plugin . "/plugin.json");
                                $pdata = json_decode($pdata,true);
                                if(isset($pdata[0]['contextmenu'])) {
                                    foreach($pdata[0]['contextmenu'] as $contextmenu) {
                                        if((!isset($contextmenu['admin']) || ($contextmenu['admin']) && checkAccess()) || !$contextmenu['admin']){
                                            if(isset($contextmenu['applies-to']) && isset($contextmenu['action']) && isset($contextmenu['icon']) && isset($contextmenu['title'])) {
                                                echo('<hr class="'.$contextmenu['applies-to'].'">');
                                                echo('<a class="'.$contextmenu['applies-to'].'" onclick="'.$contextmenu['action'].'"><span class="'.$contextmenu['icon'].'"></span>'.$contextmenu['title'].'</a>');
                                            }
                                        }
                                    }
                                }
                            }
                        }
                ?>

                </div>

                <div id="file-manager"></div>

                <ul id="list-active-files"></ul>

            </div>
            
            <div id="side-projects" class="sb-left-projects">
                <div id="project-list" class="sb-project-list">
                
                    <div class="project-list-title">
                        <h2><?php i18n("Projects"); ?></h2>
                        <a id="projects-collapse" class="icon-down-dir icon" alt="<?php i18n("Collapse"); ?>"></a>
                        <?php if(checkAccess()) { ?>
                        <a id="projects-manage" class="icon-archive icon"></a>
                        <a id="projects-create" class="icon-plus icon" alt="<?php i18n("Create Project"); ?>"></a>
                        <?php } ?>
                    </div>
                    
                    <div class="sb-projects-content"></div>
                    
                </div>
            </div>

            <div class="sidebar-handle"><span>||</span></div>
            </div>
        </div>

        <div id="cursor-position"><?php i18n("Ln"); ?>: 0 &middot; <?php i18n("Col"); ?>: 0</div>

        <div id="editor-region">
            
            <div class="menu-tools-bg">				
				<div class="right-menu-title">
					<a href="#" class="login-link"><i class="fa fa-cog" aria-hidden="true"></i>&nbsp; Compile</a> | 
					<a href="#" class="login-link"><i class="fa fa-cogs" aria-hidden="true"></i>&nbsp; Execute</a> | 
					<a href="#" class="login-link"><i class="fa fa-share-alt" aria-hidden="true"></i>&nbsp; Share</a>
				</div>		
			</div>
            
            <div id="editor-top-bar">
                <ul id="tab-list-active-files"> </ul>
                <div id="tab-dropdown">
                    <a id="tab-dropdown-button" class="icon-down-open"></a>
                </div>
                <div id="tab-close">
                    <a id="tab-close-button" class="icon-cancel-circled" title="<?php i18n("Close All") ?>"></a>
                </div>
                <ul id="dropdown-list-active-files"></ul>
                <div class="bar"></div>
            </div>

            <div id="root-editor-wrapper"></div>

            <div id="editor-bottom-bar">
                <a id="settings" class="ico-wrapper"><span class="icon-doc-text"></span><?php i18n("Settings"); ?></a>
                
                <?php

                    ////////////////////////////////////////////////////////////
                    // Load Plugins
                    ////////////////////////////////////////////////////////////
                    
                    //print_r($plugins);
                    foreach ($plugins as $plugin){
                        if(file_exists(PLUGINS . "/" . $plugin . "/plugin.json")) {
                            $pdata = file_get_contents(PLUGINS . "/" . $plugin . "/plugin.json");
                            $pdata = json_decode($pdata,true);
                            if(isset($pdata[0]['bottombar'])) {
                                foreach($pdata[0]['bottombar'] as $bottommenu) {
                                    if((!isset($bottommenu['admin']) || ($bottommenu['admin']) && checkAccess()) || !$bottommenu['admin']){
                                        if(isset($bottommenu['action']) && isset($bottommenu['icon']) && isset($bottommenu['title'])) {
                                            echo('<div class="divider"></div>');
                                            echo('<a onclick="'.$bottommenu['action'].'"><span class="'.$bottommenu['icon'].'"></span>'.$bottommenu['title'].'</a>');
                                        }
                                    }
                                }
                            }
                        }
                    }

                ?>
                
                <div class="divider"></div>
                <a id="split" class="ico-wrapper"><span class="icon-layout"></span><?php i18n("Split"); ?></a>
                <div class="divider"></div>
                <a id="current-mode"><span class="icon-layout"></span></a>                
                <div class="divider"></div>
                <div id="current-file"></div>
            </div>
            <div id="changemode-menu" class="options-menu">
            </div>
            <ul id="split-options-menu" class="options-menu">
              <li id="split-horizontally"><a> <?php i18n("Split Horizontally"); ?> </a></li>
              <li id="split-vertically"><a> <?php i18n("Split Vertically"); ?> </a></li>
              <li id="merge-all"><a> <?php i18n("Merge all"); ?> </a></li>
            </ul>
        </div>

        <div id="sb-right" class="sidebar">

            <div class="sidebar-handle"><span><a class="icon-menu"></a></span></div>
            <div id="sb-right-title">
                <span id="lock-right-sidebar" class="icon-switch icon"></span>
            </div>

            <div class="sb-right-content">

                <?php

                ////////////////////////////////////////////////////////////
                // Load Right Bar
                ////////////////////////////////////////////////////////////

                foreach($right_bar as $item_rb=>$data){
                   // print_r($data);
                    if(!isset($data['admin'])) {
                      $data['admin'] = false;
                    }
                    if($data['title']=='break'){
                        if(!$data['admin'] || $data['admin'] && checkAccess()) {
                            echo("<hr>");
                        }
                    }else if($data['title']!='break' && $data['title']!='pluginbar' && $data['onclick'] == ''){
                        if(!$data['admin'] || $data['admin'] && checkAccess()) {
                            echo("<hr><div class='sb-right-category'>".get_i18n($data['title'])."</div>");
                        }
                    }else if ($data['title']=='pluginbar'){
                        if(!$data['admin'] || $data['admin'] && checkAccess()) {
                            foreach ($plugins as $plugin){
                                if(file_exists(PLUGINS . "/" . $plugin . "/plugin.json")) {
                                    $pdata = file_get_contents(PLUGINS . "/" . $plugin . "/plugin.json");
                                    $pdata = json_decode($pdata,true);
                                    if(isset($pdata[0]['rightbar'])) {
                                        foreach($pdata[0]['rightbar'] as $rightbar) {
                                            if((!isset($rightbar['admin']) || ($rightbar['admin']) && checkAccess()) || !$rightbar['admin']){
                                                if(isset($rightbar['action']) && isset($rightbar['icon']) && isset($rightbar['title'])) {
                                                    echo('<a onclick="'.$rightbar['action'].'"><span class="'.$rightbar['icon'].'"></span>'.get_i18n($rightbar['title']).'</a>');
                                                }
                                            }
                                        }
                                        //echo("<hr>");
                                    }
                                }
                            }
                        }
                    } else{
                        if(!$data['admin'] || $data['admin'] && checkAccess()) {
                            if(isset($_SESSION) && $_SESSION['user'] =='admin'){
                                echo('<a onclick="'.$data['onclick'].'"><span class="'.$data['icon'].' bigger-icon"></span>'.get_i18n($data['title']).'</a>');
                            }else{
                                if(isset($data['title']) && $data['title']!='Users'){
                                    echo('<a onclick="'.$data['onclick'].'"><span class="'.$data['icon'].' bigger-icon"></span>'.get_i18n($data['title']).'</a>');
                                }
                            }
                        }
                    }

                }

                ?>

            </div>

        </div>

    </div>

    <div id="modal-overlay"></div>
    <div id="modal"><div id="close-handle" class="icon-cancel" onclick="codiad.modal.unload();"></div><div id="drag-handle" class="icon-location"></div><div id="modal-content" class="modalbg"></div></div>

    <iframe id="download"></iframe>

    <div id="autocomplete"><ul id="suggestions"></ul></div>

    <!-- ACE -->
   <!--  <script src="components/editor/ace-editor/ace.js"></script>

    <!-- COMPONENTS -->
    <?php

        //////////////////////////////////////////////////////////////////
        // LOAD COMPONENTS
        //////////////////////////////////////////////////////////////////

        // JS
        // foreach($components as $component){
        //     if(file_exists(COMPONENTS . "/" . $component . "/init.js")){
        //         echo('<script src="components/'.$component.'/init.js"></script>"');
        //     }
        // }
        
        // foreach($plugins as $plugin){
        //     if(file_exists(PLUGINS . "/" . $plugin . "/init.js")){
        //         echo('<script src="plugins/'.$plugin.'/init.js"></script>"');
        //     }
        // }

    }

    ?> -->
 <?php 
require_once('footer.php');
?>

</body>
</html>
