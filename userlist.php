<?php


    //////////////////////////////////////////////////////////////////
    // Verify Session or Key
    //////////////////////////////////////////////////////////////////

require_once('header_new.php');
checkSession(); 
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

.tealgn{
	text-align: center;
}
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
                <p class="list-titel">All your users</p>
                <div class="col-xs-12 col-sm-12 col-md-12 create-tab">
                    <a>
                       <button type="button" class="btn btn-Default" onclick="codiad.user.createNew();">New Account</button>
                    </a>
                    <a href="#">
                        <button type="button" class="btn btn-Default" disabled="">Import</button>
                    </a>
                </div>
                <div class="table-responsive table-bg" id="project-list">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th class="tealgn"><?php i18n("Usename"); ?></th>
								<th class="tealgn"><?php i18n("Email"); ?></th>
								<th class="tealgn"><?php i18n("Organisation"); ?></th>
								<th class="tealgn"><?php i18n("City"); ?></th>
                                <th class="tealgn"><?php i18n("Password"); ?></th>
                                <th class="tealgn"><?php i18n("Projects"); ?></th>
                                <?php if(checkAccess()){ ?>
                                    <th class="tealgn"><?php i18n("Delete"); ?></th>
                                <?php } ?>
                            </tr>
                        </thead>
                        <tbody>
                        <?php
							// Get projects JSON data
							$users = getJSON('users.php');
							foreach($users as $user=>$data){
						?>
								<tr class="tealgn">
									<td>
                                        <?php echo($data['username']); ?>
                                    </td>
									<td>
										<?php if($data['email'] != null){echo($data['email']); }else{ echo "Data not Provided by user"; }?>
									</td>
									<td>
										<?php echo($data['organization']); ?>
									</td>
									<td>
										<?php echo($data['city']); ?>
									</td>
                                    <td><a onclick="codiad.user.password('<?php echo($data['username']); ?>');" class="icon-flashlight bigger-icon"></a></td>
                                    <td><a onclick="codiad.user.projects('<?php echo($data['username']); ?>');" class="icon-archive bigger-icon"></a></td>
									<?php
									if($_SESSION['user'] == $data['username']){
									?>
									<td width="75"><a onclick="codiad.message.error('You Cannot Delete Your Own Account');" class="icon-block bigger-icon"></a></td>
									<?php
									}else{
									?>
									<td width="70"><a onclick="codiad.user.delete('<?php echo($data['username']); ?>');" class="icon-cancel-circled bigger-icon"></a></td>
									<?php
									}
									?>
                                </tr>
                        <?php
							}
						?>
                            </tbody>
                        </table>
                    </div>

                    <p>&nbsp;</p>
                    <p>&nbsp;</p>
                    <p>&nbsp;</p>
                    <p>&nbsp;</p>

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