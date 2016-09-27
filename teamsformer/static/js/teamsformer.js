
$(document).ready(function(){
// Tooltip
    $('[data-toggle="tooltip"]').tooltip();
    
// Popuo
    $('[data-toggle="popover"]').popover();
   
// Enable configure the profile
    $('#config-enable').click(function(){
		$('.profile-form input, textarea, select, button').attr("disabled", false);
		$(this).removeClass('btn-default').addClass('btn-success');
		});
		
// Active links
	$('.nav li a').each(function(){
		if (this.href == window.location.href){
			$(this).parents('li').addClass('active');
			}
		if (window.location.href.search(this.href) > -1) {
			$(this).parents('li').addClass('active');
			};
		});
		

// Scroll dialog list
		$('.dialogs').ready(function(){
			$('.dialog').animate({
				scrollTop: 9999 }, 'slow');
			});

});
