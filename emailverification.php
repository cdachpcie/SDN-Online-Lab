<?php

  /*
    *  Copyright (c) C-DAC
    */

    require_once('common.php');
    require_once('components/user/class.user.php');
    
    
if(isset($_SERVER['QUERY_STRING'])){
    
    $sring = $_SERVER['QUERY_STRING'];
    $str = explode("&",$sring);
    $strun = explode("=",$str[0]);
    $hashid = $str[1];
    $uname = $strun[1];
    $User = new User();
    $User->username = $uname;
    $User->hashid = $hashid;
    $User->status = 1;
    $status = $User->Status($uname,$hashid);
}else{
    header("Location: http://localhost/404.php");
    exit;
}
?>