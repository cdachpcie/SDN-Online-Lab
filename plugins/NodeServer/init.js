(function(global, $){

    
    var codiad = global.codiad,
        scripts = document.getElementsByTagName('script'),
        path = scripts[scripts.length-1].src.split('?')[0],
        curpath = path.split('/').slice(0, -1).join('/')+'/';

    
    codiad.mininetEditor = {
        
        path: curpath,

        init: function() {

            // Start your plugin here...

        },

        /**
         *
         * This is where the core functionality goes, any call, references,
         * script-loads, etc...
         *
         */
         
         open: function() {
            window.open('http://127.0.0.1:8081');
         }

    };

})(this, jQuery);



