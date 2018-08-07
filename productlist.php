 
<?php

  //require_once('common.php');
    
    //////////////////////////////////////////////////////////////////
    // Verify Session or Key
    //////////////////////////////////////////////////////////////////

require_once('header_new.php');
checkSession(); 
//$_SESSION['lang'] ='en';
//echo '<pre>';print_r($_SESSION);die;

            $projects_assigned = false;
            if(file_exists(BASE_PATH . "/data/" . $_SESSION['user'] . '_acl.php')){
                $projects_assigned = getJSON($_SESSION['user'] . '_acl.php');
            }
            
            ?>
            
            	<style>
	
.modal-content-set {
  position: relative;
  background-color: #fff;
  -webkit-background-clip: padding-box;
          background-clip: padding-box;
  border: 1px solid #999;
  border: 1px solid rgba(0, 0, 0, .2);
  border-radius: 6px;
  outline: 0;
  -webkit-box-shadow: 0 3px 9px rgba(0, 0, 0, .5);
          box-shadow: 0 3px 9px rgba(0, 0, 0, .5);
}

@media (min-width: 768px) {
  .modal-dialog-set {
    width: 800px;
    margin: 30px auto;
  }
  .modal-content-set {
    -webkit-box-shadow: 0 5px 15px rgba(0, 0, 0, .5);
            box-shadow: 0 5px 15px rgba(0, 0, 0, .5);
  }
	
.modal-body-set {
  position: relative;
  padding: 15px;
  min-height:300px;
  overflow:auto;
}	


.tabs-left > .nav-tabs {
    float: left;
    margin-right: 19px;
    border: none;
}

.tabs-below > .nav-tabs, .tabs-right > .nav-tabs, .tabs-left > .nav-tabs {
    border-bottom: 0;
}

.tabs-left > .nav-tabs > li, .tabs-right > .nav-tabs > li {
    float: none;
}

.tabs-left > .nav-tabs > li > a {
    margin-right: -1px;
    -webkit-border-radius: 4px 0 0 4px;
    -moz-border-radius: 4px 0 0 4px;
    border-radius: 4px 0 0 4px;
}
.tabs-left > .nav-tabs > li > a, .tabs-right > .nav-tabs > li > a {
    min-width: 74px;
    margin-right: 0;
    margin-bottom: 3px;
    background-color: #6ac0de;
    border-radius:0px;
    color: white;
}

.tabs-left > .nav-tabs .active > a, .tabs-left > .nav-tabs .active > a:hover, .tabs-left > .nav-tabs .active > a:focus {
    border-color: #ddd transparent #ddd #ddd;
	    background-color: #f8f8f8;
color: dimgrey;
border:none;
}

.left-tab-process .tab-content{
	background-color:#f8f8f8;
	   margin-left: 115px;
		overflow:x scroll;}

.tab-content > .active, .pill-content > .active {
    display: block;
}

.book-process-ltab{
	max-width:135px;}
	
.left-tab-process .tab-pane{
    padding: 11px 32px;
    min-height: 300px;
}

.left-tab-process h4{
	color:#536779;}
	
.term-fa{
margin-right: 7px;
    font-size: 11px;
    margin-left: -18px;
    color: #2EA72F;}
    
.tac-content{
    background-color:#ccc;}
	
	

	
	</style>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]> -->
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
      
<div class="container-fluid" style="width: 100%;position: absolute;">
    <div class="row">
        <!--main panal Start-->
        <div class="list">
            <div class="list-bg">
                <p class="list-titel">All your projects</p>
                <div class="col-xs-12 col-sm-12 col-md-12 create-tab">
                    <a id="projects-create">
                       <button type="button" class="btn btn-Default" data-toggle="modal" data-target="#create">Create</button>
                    </a>
                    <a href="#">
                        <button type="button" class="btn btn-Default" disabled="">Import</button>
                    </a>
                </div>
                <div class="table-responsive table-bg" id="project-list">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th><?php i18n("Open"); ?></th>
                                <th><?php i18n("Project Name"); ?></th>
                                <th><?php i18n("Path"); ?></th>
                                <?php if(checkAccess()){ ?>
                                    <th><?php i18n("Delete"); ?></th>
                                <?php } ?>
                            </tr>
                        </thead>
                        <tbody>
                                <?php
            
            // Get projects JSON data
			$projects = getJSON('projects.php');
            sort($projects);
            
            function filter_by_value ($array, $index, $value){
                if(is_array($array) && count($array)>0) 
                {
                    foreach(array_keys($array) as $key){
                        $temp[$key] = $array[$key][$index];
                        
                        if ($temp[$key] == $value){
                            $newarray[$key] = $array[$key];
                        }
                    }
                  }
                  if(isset($newarray) && $newarray !=''){
                    return $newarray;
                  }
      
            }
			
			//print_r($projects);
		
        $nResults = filter_by_value($projects, 'username', $_SESSION['user']);
            
        if(isset($_SESSION) && $_SESSION['user'] != 'admin'){
    
            $projects = $nResults;
			
        }
        if(($projects) && $projects != ''){
            foreach($projects as $project=>$data){
                $show = true;
                if($projects_assigned && !in_array($data['path'],$projects_assigned)){ $show=false; }
               // if($show){
					//print_r($projects);
                ?>
                                <tr>
                                    <td>
                                        <a onclick="codiad.project.open('<?php echo($data['path']); ?>');" class="icon-folder bigger-icon">
                                        </a>
                                    </td>
                                    <td>
                                        <?php echo($data['name']); ?>
                                    </td>
                                    <td>
                                        <?php echo($data['path']); ?>
                                    </td>
                                    <?php
                        if(checkAccess()){
                            if($_SESSION['project'] == $data['path']){
                            ?>
                                    <td>
                                        <a onclick="codiad.message.error(i18n('Active Project Cannot Be Removed'));" class="icon-block bigger-icon"></a>
                                    </td>
                                    <?php
                            }else{
                            ?>
                                    <td>
                                        <a onclick="codiad.project.delete('<?php echo($data['name']); ?>','<?php echo($data['path']); ?>');" class="icon-cancel-circled bigger-icon">
                                        </a>
                                    </td>
                                    <?php
                            }
                        }
                    ?>
                                </tr>
                                <?php
                //}
            }
           
		   
		}else{
			
			echo "You have not created any project yet. To create project click on create button";
			
			} ?>
                            </tbody>
                        </table>
                    </div>

                    <p>&nbsp;</p>
                    <p>&nbsp;</p>
                    <p>&nbsp;</p>
                    <p>&nbsp;</p>
                    <!--   
                    <?//php if(checkAccess()){ ?><button class="btn-left" onclick="codiad.project.create();">
                    <?//php i18n("New Project"); ?></button>
                    <?//php } ?><button class="
                    <?//php if(checkAccess()){ echo('btn-right'); } ?>" onclick="codiad.modal.unload();return false;">
                    <?//php i18n("Close"); ?></button> -->
					
					   <div id="modal-overlay"></div>
						<div id="modal"><div id="close-handle" class="icon-cancel" onclick="codiad.modal.unload();"></div><div id="drag-handle" class="icon-location"></div><div id="modal-content" class="modalbg"></div></div>
					
						<iframe id="download"></iframe>
					
						<div id="autocomplete"><ul id="suggestions"></ul></div>
                  
                </div>
            </div>  
        </div>
    </div>




<!-- Modal -->
<div id="create" class="modal fade" role="dialog">
  <div class="modal-dialog">

    <!-- Modal content-->
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h3 class="modal-title">Create New Project</h3>
      </div>
      <div class="modal-body">
		<form class="form-horizontal">
		  <div class="form-group">
			<label class="col-sm-3 control-label">Project Name</label>
			<div class="col-sm-9">
			  <input type="email" class="form-control" id="inputEmail3" placeholder="Project Name">
			</div>
		  </div>
		  <div class="form-group">
			<label class="col-sm-3 control-label">Folder Name</label>
			<div class="col-sm-9">
			  <input type="email" class="form-control" id="inputEmail3" placeholder="Folder Name">
			</div>
		  </div>
		</form>
      </div>
      <div class="modal-footer">
	  	<button type="button" class="btn btn-success" data-toggle="modal" data-target="#create1">Create</button>
		<button type="button" class="btn btn-info">Git Repo</button>
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>

  </div>
</div>
<!-- End Modal -->


<!-- 2 Modal -->
<div id="create1" class="modal fade" role="dialog">
  <div class="modal-dialog">

    <!-- Modal content-->
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h3 class="modal-title">Create New Project</h3>
      </div>
      <div class="modal-body">
        
			<form class="form-horizontal">
			  <div class="form-group">
				<label class="col-sm-3 control-label">Project Name</label>
				<div class="col-sm-9">
				  <input type="email" class="form-control" id="inputEmail3" placeholder="Project Name">
				</div>
			  </div>
			  <div class="form-group">
				<label class="col-sm-3 control-label">Folder Name</label>
				<div class="col-sm-9">
				  <input type="email" class="form-control" id="inputEmail3" placeholder="Folder Name">
				</div>
			  </div>
			  <div class="form-group">
				<label class="col-sm-3 control-label">Git Repository</label>
				<div class="col-sm-9">
				  <input type="email" class="form-control" id="inputEmail3" placeholder="Git Repository">
				</div>
			  </div>
			  <div class="form-group">
				<label class="col-sm-3 control-label">Branch</label>
				<div class="col-sm-9">
				  <input type="email" class="form-control" id="inputEmail3" placeholder="Branch">
				</div>
			  </div>
			</form>

      </div>
      <div class="modal-footer">
	  	<button type="button" class="btn btn-success">Create</button>
		<button type="button" class="btn btn-info">Git Repo</button>
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>

  </div>
</div>
<!-- End 2 Modal -->




<!-- Setting Modal -->
<div id="setting" class="modal fade" role="dialog">
  <div class="modal-dialog-set">

    <!-- Modal content-->
    <div class="modal-content-set">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h3 class="modal-title">Settings</h3>
      </div>
      <div class="modal-body-set">
        
						<div class="tabbable tabs-left left-tab-process" style="margin-bottom:25px;">
                              <ul class="nav nav-tabs book-process-ltab">
                                              <li class="active"><a href="#a" data-toggle="tab"><i class="fa fa-home" aria-hidden="true"></i> Editor</a></li>
                                              <li class=""><a href="#b" data-toggle="tab"><i class="fa fa-desktop" aria-hidden="true"></i> System</a></li>
                                              <li class=""><a href="#c" data-toggle="tab"><i class="fa fa-pencil" aria-hidden="true"></i> Extensions</a></li>
                                              
                                </ul>
                                <div class="tab-content">
                                     <div class="tab-pane active" id="a">
                                          <p><b><i class="fa fa-home" aria-hidden="true"></i> Editor</b></p>  <hr>  
										
										<form class="form-horizontal">
										 
											<div class="form-group">											
											  <label for="TextInput" class="col-sm-4">Theme</label>
											  	<div class="col-sm-6">
													<select class="form-control">
													  <option>1</option>
													  <option>2</option>
													  <option>3</option>
													  <option>4</option>
													  <option>5</option>
													</select>     
												</div>										
											</div>
										
											
										</form>
						
											   
                                     </div>
                                     <div class="tab-pane" id="b">
										<p><b><i class="fa fa-desktop" aria-hidden="true"></i> System</b></p>  <hr>
											
											
                                      </div>
                                      <div class="tab-pane" id="c">
                                           <p><b><i class="fa fa-pencil" aria-hidden="true"></i> Extensions</b></p>  <hr>
										   
                                       </div>
											 
                                            </div>
                                          </div>

      </div>
      <div class="modal-footer">
	  	<button type="button" class="btn btn-success">Create</button>
		<button type="button" class="btn btn-info">Git Repo</button>
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>

  </div>
</div>
<!-- End Setting Modal -->

<script src="js/custom.js"></script>
    
              <?php 
require_once('footer.php');
?>