/*
 *  Copyright (c) C-DAC
 */

(function(global, $){

    var codiad = global.codiad;

    $(function() {
        codiad.project.init();
    });

    codiad.project = {

        controller: 'components/project/controller.php',
        dialog: 'components/project/dialog.php',

        init: function() {
            this.loadCurrent();
            this.loadSide();
            
            var _this = this;
            
            $('#projects-create').click(function(){
                codiad.project.create('true');
            });
            
            $('#projects-manage').click(function(){
                codiad.project.list();
            });
            
            $('#projects-collapse').click(function(){
                if (!_this._sideExpanded) {
                    _this.projectsExpand();
                } else {
                    _this.projectsCollapse();
                }
            });
        },

        //////////////////////////////////////////////////////////////////
        // Get Current Project
        //////////////////////////////////////////////////////////////////

        loadCurrent: function() {
            $.get(this.controller + '?action=get_current', function(data) {
                var projectInfo = codiad.jsend.parse(data);
                if (projectInfo != 'error') {
                    $('#file-manager')
                        .html('')
                        .append('<div class="container tree-bg" style="margin-top:0px;"><ul><li><a id="project-root" data-type="root" class="directory fontColor" data-path="' + projectInfo.path + '">' + projectInfo.name + '</a></li></ul></div>');
                    codiad.filemanager.index(projectInfo.path);
                    codiad.user.project(projectInfo.path);
                    codiad.message.success(i18n('Project %{projectName}% Loaded', {projectName:projectInfo.name}));
                }
            });
        },

        //////////////////////////////////////////////////////////////////
        // Open Project
        //////////////////////////////////////////////////////////////////

        open: function(path) {
            var base_url = window.location.origin;
         //   alert(base_url);
            var _this = this;
            codiad.finder.contractFinder();
            $.get(this.controller + '?action=open&path=' + encodeURIComponent(path), function(data) {
                var projectInfo = codiad.jsend.parse(data);
                if (projectInfo != 'error') {
                    _this.loadCurrent();
                    codiad.modal.unload();
                    codiad.user.project(path);
                    localStorage.removeItem("lastSearched");
                    /* Notify listeners. */
                    amplify.publish('project.onOpen', path);
                    window.location.href = base_url;

                }
            });
        },

        //////////////////////////////////////////////////////////////////
        // Open the project manager dialog
        //////////////////////////////////////////////////////////////////

        list: function() {
            $('#modal-content form')
                .die('submit'); // Prevent form bubbling
            codiad.modal.load(500, this.dialog + '?action=list');
        },
        
        //////////////////////////////////////////////////////////////////
        // Load and list projects in the sidebar.
        //////////////////////////////////////////////////////////////////
        loadSide: function() {
            $('.sb-projects-content').load(this.dialog + '?action=sidelist&trigger='+localStorage.getItem('codiad.editor.fileManagerTrigger'));
            this._sideExpanded = true;
        },
        
        projectsExpand: function() {
            this._sideExpanded = true;
            $('#side-projects').css('height', 276+'px');
            $('.project-list-title').css('right', 0);
            $('.sb-left-content').css('bottom', 276+'px');
            $('#projects-collapse')
                .removeClass('icon-up-dir')
                .addClass('icon-down-dir');
        },
        
        projectsCollapse: function() {
            this._sideExpanded = false;
            $('#side-projects').css('height', 33+'px');
            $('.project-list-title').css('right', 0);
            $('.sb-left-content').css('bottom', 33+'px');
            $('#projects-collapse')
                .removeClass('icon-down-dir')
                .addClass('icon-up-dir');
        },
        
        //////////////////////////////////////////////////////////////////
        // Create Project
        //////////////////////////////////////////////////////////////////

        create: function(close) {
            var _this = this;
            create = true;
            codiad.modal.load(500, this.dialog + '?action=create&close=' + close);
            $('#modal-content form')
                .live('submit', function(e) {
              //      alert('hi');
                e.preventDefault();
                var projectName = $('#modal-content form input[name="project_name"]')
                    .val(),
                    projectPath = $('#modal-content form input[name="project_path"]')
                    .val(),
                    userName = $('#modal-content form input[name="user_name"]')
                    .val(),
                    gitRepo = $('#modal-content form input[name="git_repo"]')
                    .val(),
                    gitBranch = $('#modal-content form input[name="git_branch"]')
                    .val();
                    if(projectPath.indexOf('/') == 0) {
                        create = confirm('Do you really want to create project with absolute path "' + projectPath + '"?');
                    }
                if(create) {
                //    alert(userName);
                    $.get(_this.controller + '?action=create&project_name=' + encodeURIComponent(projectName) + '&user_name=' + encodeURIComponent(userName) + '&project_path=' + encodeURIComponent(projectPath) + '&git_repo=' + gitRepo + '&git_branch=' + gitBranch, function(data) {
                        createResponse = codiad.jsend.parse(data);
                 //       alert(data)
                        if (createResponse != 'error') {
                            _this.list();
                             location.reload(); 
                          //  _this.open(createResponse.path);
                            codiad.modal.unload();
                            _this.loadSide();
                            /* Notify listeners. */
                            amplify.publish('project.onCreate', {"name": projectName, "username" : userName, "path": projectPath, "git_repo": gitRepo, "git_branch": gitBranch});
                        }
                    });
                }
            });
        },
        
        //////////////////////////////////////////////////////////////////
        // Rename Project
        //////////////////////////////////////////////////////////////////

        rename: function(path,name) {
            var _this = this;
            codiad.modal.load(500, this.dialog + '?action=rename&path=' + encodeURIComponent(path) + '&name='+name);
            $('#modal-content form')
                .live('submit', function(e) {
                e.preventDefault();
                var projectPath = $('#modal-content form input[name="project_path"]')
                    .val();
                var projectName = $('#modal-content form input[name="project_name"]')
                    .val();    
                $.get(_this.controller + '?action=rename&project_path=' + encodeURIComponent(projectPath) + '&project_name=' + encodeURIComponent(projectName), function(data) {
                   renameResponse = codiad.jsend.parse(data);
                    if (renameResponse != 'error') {
                        codiad.message.success(i18n('Project renamed'));
                        _this.loadSide();
                        $('#file-manager a[data-type="root"]').html(projectName);
                        codiad.modal.unload();
                        /* Notify listeners. */
                        amplify.publish('project.onRename', {"path": projectPath, "name": projectName});
                    }
                });
            });
        },
        
        //////////////////////////////////////////////////////////////////
        // Delete Project
        //////////////////////////////////////////////////////////////////

        delete: function(name, path) {
            var _this = this;
            codiad.modal.load(500, this.dialog + '?action=delete&name=' + encodeURIComponent(name) + '&path=' + encodeURIComponent(path));
            $('#modal-content form')
                .live('submit', function(e) {
                e.preventDefault();
                var projectPath = $('#modal-content form input[name="project_path"]')
                    .val();
                var deletefiles = $('input:checkbox[name="delete"]:checked').val();
                var followlinks = $('input:checkbox[name="follow"]:checked').val();
                var action = '?action=delete';
                if( typeof deletefiles !== 'undefined' ) {
                    if( typeof followlinks !== 'undefined' ) {
                        action += '&follow=true&path=' + encodeURIComponent(projectPath);
                    } else {
                        action += '&path=' + encodeURIComponent(projectPath);
                    }
                }
                $.get(codiad.filemanager.controller + action, function(d) {
                    $.get(_this.controller + '?action=delete&project_path=' + encodeURIComponent(projectPath), function(data) {
                        deleteResponse = codiad.jsend.parse(data);
                        if (deleteResponse != 'error') {
                            codiad.message.success(i18n('Project Deleted'));
                            _this.list();
                            _this.loadSide();
                            // Remove any active files that may be open
                            $('#active-files a')
                                .each(function() {
                                var curPath = $(this)
                                    .attr('data-path');
                                if (curPath.indexOf(projectPath) == 0) {
                                    codiad.active.remove(curPath);
                                }
                            });
                            /* Notify listeners. */
                            amplify.publish('project.onDelete', {"path": projectPath, "name": name});
                            location.reload(); 
                        }
                    });
                });
            });
        },
        
        //////////////////////////////////////////////////////////////////
        // Check Absolute Path
        //////////////////////////////////////////////////////////////////
        
        isAbsPath: function(path) {
            if ( path.indexOf("/") == 0 ) {
                return true;
            } else {
                return false;
            }
        },

        //////////////////////////////////////////////////////////////////
        // Get Current (Path)
        //////////////////////////////////////////////////////////////////

        getCurrent: function() {
            var _this = this;
            var currentResponse = null;
            $.ajax({
                url: _this.controller + '?action=current',
                async: false,
                success: function(data) {
                    currentResponse = codiad.jsend.parse(data);
                } 
             });
            return currentResponse;
        }
    };
})(this, jQuery);
