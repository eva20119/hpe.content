// PORTFOLIO FILTERING - ISOTOPE
//**********************************
jQuery.noConflict()(function($){
"use strict";

		$('body').on('touchstart','.st_sf_strange_portfolio_item', function () {
			$(this).trigger('hover');
		}).on('touchend','.st_sf_strange_portfolio_item', function () {
			$(this).trigger('hover');
		});
	var $container = $('div:not(.st_sf_f_t_wo_s)>.st_sf_port_container');
	if($container.length) {
		//$('.st_sf_portfolio_page_holder').css('min-height',$(window).height())
		$container.waitForImages(function() {
			
			// initialize isotope
			$container.isotope({
			  itemSelector : '.st_sf_strange_portfolio_item',
			  layoutMode : 'masonry',
			});
			
			$('#filters li:first-child').addClass('current-cat');
			// filter items when filter link is clicked
			$('#filters a').click(function(){
			  var selector = $(this).attr('data-filter');
			  $container.isotope({ filter: selector });
			  $(this).parent('li').addClass('current-cat').siblings().removeClass('current-cat');
			  
			  return false;
			});
			
			
			
		},null,true);
	
	}
	
var $containerr = $('.st_sf_posts_ul.st_sf_ul_will_be_masonry');
	if($containerr.length) {
		//$('.st_sf_portfolio_page_holder').css('min-height',$(window).height())
		$containerr.waitForImages(function() {
			
			// initialize isotope
			$containerr.isotope({
			  itemSelector : '.st_sf_format_will_be_masonry',
			  layoutMode : 'masonry',
			});
			
		},null,true);
	
	}
});

