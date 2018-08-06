<?php

    /*
    *  Copyright (c) Codiad & Kent Safranski (codiad.com), distributed
    *  as-is and without warranty under the MIT License. See 
    *  [root]/license.txt for more. This information must remain intact.
    */


    require_once('../../common.php');
    
    //////////////////////////////////////////////////////////////////
    // Verify Session or Key
    //////////////////////////////////////////////////////////////////
    
    checkSession();
	//echo '<pre>';
	// Outputs all the result of shellcommand "ls", and returns
	// the last output line into $last_line. Stores the return value
	// of the shell command in $retval.
	//$last_line = shell_exec('sudo /home/ubuntu/Downloads/./miniedit.py', $retval);
	// Printing additional info

    



/*//<?php
$output = system('ls -a');
//$output1 = system();
echo "<pre>$output</pre>";
?>*/

/*<?php
// outputs the username that owns the running php/httpd process
// (on a system with the "whoami" executable in the path)
$cmd = 'cd var/www/html/plugins/miniedit\ plugin/'
echo system('cmd');
//echo exec('sudo mn')
?>*/

/*<?php 

$command = escapeshellcmd('miniedit.py');
$output = shell_exec($command);
echo $output;

?>*/

//$last_line = system('python mininet/examples/miniedit.py', $retval);

//$PATH = 'python mininet/examples/miniedit.py'
//passthru ('python mininet/examples/miniedit.py');


?>


<style>#terminal { border: 1px solid #2b2b2b; }</style>
<!--<center><h2>Mininet</h2></center>-->

 <!--<iframe src="http://sdnonlinelab/test.py" width="100%" height="400"></iframe> -->
 <iframe src="http://sdnonlinelab/testdemo.php" width="100%" height="600"></iframe> 

<!--<iframe id="terminal" width="100%" height="400"></iframe>-->

<button onclick="codiad.modal.unload(); return false;">Close Mininet</button>
<script>
    $(function(){ 
        var wheight = $(window).outerHeight() * 0.5;
        $('#terminal').css('height',wheight+'px');
        $('#terminal').attr('src', codiad.terminal.path + "mininet/miniedit.php");
    });
</script>

