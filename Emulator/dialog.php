<?php

    /*
    *  Copyright (c) C-DAC
    */


    require_once('../../common.php');
    
    //////////////////////////////////////////////////////////////////
    // Verify Session or Key
    //////////////////////////////////////////////////////////////////
    
    checkSession();
?>


<style>#terminal { border: 1px solid #2b2b2b; }</style>

<iframe src="<?php echo BASE_URL; ?>/plugins/Emulator/emulator.php" width="100%" height="400"></iframe> 

<!--<iframe id="terminal" width="100%" height="400"></iframe>-->

<button onclick="codiad.modal.unload(); return false;">Close Emulator</button>
<script>
    $(function(){ 
        var wheight = $(window).outerHeight() * 0.5;
        $('#terminal').css('height',wheight+'px');
        $('#terminal').attr('src', codiad.terminal.path + "mininet/miniedit.php");
    });
</script>

