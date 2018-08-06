<?php

    /*
    *  Copyright (c) C-DAC
    */
    

    require_once('../../common.php');
    require_once('class.update.php');

    //////////////////////////////////////////////////////////////////
    // Verify Session or Key
    //////////////////////////////////////////////////////////////////

    checkSession();

    $update = new Update();
    
    //////////////////////////////////////////////////////////////////
    // Set Initial Version
    //////////////////////////////////////////////////////////////////

if ($_GET['action']=='init') {
    $update->Init();
}
    
    //////////////////////////////////////////////////////////////////
    // Clear Version
    //////////////////////////////////////////////////////////////////

if ($_GET['action']=='clear') {
    if (checkAccess()) {
        $update->Clear();
    }
}
    
    //////////////////////////////////////////////////////////////////
    // OptOut
    //////////////////////////////////////////////////////////////////

if ($_GET['action']=='optout') {
    if (checkAccess()) {
        $update->OptOut();
    }
}
