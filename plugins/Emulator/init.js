/*
 *  Copyright (c) C-DAC
 */

(function(global, $){
    
    var codiad = global.codiad,
        scripts = document.getElementsByTagName('script'),
        path = scripts[scripts.length-1].src.split('?')[0],
        curpath = path.split('/').slice(0, -1).join('/')+'/';
    
    codiad.terminal3 = {
        
        path: curpath,

        termWidth: $(window)
            .outerWidth() - 500,

        open3: function() {
            codiad.modal.load(this.termWidth, this.path+'dialog.php');
            codiad.modal.hideOverlay();
        }
        
    };
})(this, jQuery);




