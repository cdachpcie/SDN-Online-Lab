// JavaScript Document

//For Project Section Menu Start

/*$(document).ready(function(){
$(".panelToggle").click(function(){
    $(".userPanel").toggleClass("width200px width45px");
	$("i",this).toggleClass("fa-arrow-left fa-arrow-right");
	$(".userLogo img").toggleClass("width50p width90p");
	$(".userNameSpan").toggleClass("show hide");
	$(".userMenu span").toggleClass("show hide");
	$(".userMenu ul").toggleClass("showI2");
	$(".userMenu ul i").toggleClass("Icon Icon2");
});
});
*/
//For Project Section Menu End

$(document).ready(function () {
    
    $('#nav').children('li').first().children('a').addClass('active')
        .next().addClass('is-open').show();
        
    $('#nav').on('click', 'li > a', function() {
        
      if (!$(this).hasClass('active')) {

        $('#nav .is-open').removeClass('is-open').hide();
        $(this).next().toggleClass('is-open').toggle();
          
        $('#nav').find('.active').removeClass('active');
        $(this).addClass('active');
      } else {
        $('#nav .is-open').removeClass('is-open').hide();
        $(this).removeClass('active');
      }
   });
});

//For tree menu

$.fn.extend({
    treed: function (o) {
      
      var openedClass = 'glyphicon-folder-open';
      var closedClass = 'glyphicon-folder-close';
      
      if (typeof o != 'undefined'){
        if (typeof o.openedClass != 'undefined'){
        openedClass = o.openedClass;
        }
        if (typeof o.closedClass != 'undefined'){
        closedClass = o.closedClass;
        }
      };
      
        //initialize each of the top levels
        var tree = $(this);
        tree.addClass("tree");
        tree.find('li').has("ul").each(function () {
            var branch = $(this); //li with children ul
            branch.prepend("<i class='indicator glyphicon " + closedClass + "'></i> ");
            branch.addClass('branch');
            branch.on('click', function (e) {
                if (this == e.target) {
                    var icon = $(this).children('i:first');
                    icon.toggleClass(openedClass + " " + closedClass);
                    $(this).children().children().toggle();
                }
            })
            branch.children().children().toggle();
        });
        //fire event from the dynamically added icon
      tree.find('.branch .indicator').each(function(){
        $(this).on('click', function () {
            $(this).closest('li').click();
        });
      });
        //fire event to open branch if the li contains an anchor instead of text
        tree.find('.branch>a').each(function () {
            $(this).on('click', function (e) {
                $(this).closest('li').click();
                e.preventDefault();
            });
        });
        //fire event to open branch if the li contains a button instead of text
        tree.find('.branch>button').each(function () {
            $(this).on('click', function (e) {
                $(this).closest('li').click();
                e.preventDefault();
            });
        });
    }
});

//Initialization of treeviews

$('#tree1').treed();

$('#tree2').treed({openedClass:'glyphicon-folder-open', closedClass:'glyphicon-folder-close'});

$('#tree3').treed({openedClass:'glyphicon-chevron-right', closedClass:'glyphicon-chevron-down'});


//For tree menu end