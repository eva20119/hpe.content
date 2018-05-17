jQuery.noConflict()(function ($) {
	"use strict";

/* 應該寫在custom.js的，寫在這裏比較快 */
$(document).ready(function(){

// 主選單，還沒有的連結無效化
    $("ul.primary-menu li a[href='singin']").attr('href', 'javascript:void(0)')

// 中文ch 改為 中文Tw
    $("option[value='ch'], option[value='chinese']").text('中文Tw')

// 上傳照片，還沒開始，連結無效化及alert
    $(".shoping_cart_icon a.my_shop_icon[href='http://hpe.mingtak.com.tw/upload']").attr('href', 'javascript:void(0)')
    $('.shoping_cart_icon .my_shop_icon .fa-thumbs-o-up').click(function(){
        alert('活動尚未開始')
    })


})




	$('body').css('min-height', $(window).outerHeight() + 1);
	$('section.not-found').css('min-height', $(window).outerHeight() + 1);
	/*************************************/
	/*MENU*/
	$('.primary-menu >li.menu-item-has-children > a').click(function (e) {
		$(this).parent().find(' > ul').prepend('<li class="oi_go_back"><span><i class="fa fa-long-arrow-left"> <em>Go Back</em></i>  ' + $(this).html() + '</span></li>');
		$(this).parent().parent().find('> li > a').animate({
			'opacity': 0
		}, 100);
		$(this).parent().find('> ul').css('display', 'block').animate({
			'opacity': 1,
			'margin-left': 0
		}, 400);

		$('.oi_go_back').click(function () {
			$(this).parent().animate({
				'opacity': 0
			}, 100).css('display', 'none').css('margin-left', '200px');
			$(this).parent().parent().parent().find('>li > a').animate({
				'opacity': 1
			}, 100);
			$(this).remove();
		});
		e.preventDefault();
	});
	/*END ---- MENU*/
	/*************************************/

	$(window).load(function () {
		$('.preload').addClass('page_loaded');
		setTimeout(function () {
			$('.preload').css('display', 'none');
		}, 300);
	});
	if (($(window).width() > 1200) && ($(window).height() > 800)) {
		$("#pagepiling > .ppslide").each(function (index) {
			$(this).wrap(function () {
				return "<div class='section' data-id=" + (index + 1) + "></div>";
			});
		});
		$(window).load(function () {
			if ($('#pagepiling').length) {
				$('#pagepiling').pagepiling({
					verticalCentered: true,
					css3: false,
					scrollingSpeed: 700,
					onLeave: function (index, nextIndex, direction) {
						$('.hamburger_holder span').toggleClass('moving');
						var new_title = $('.section[data-id="' + nextIndex + '"]').find('.ppslide').attr('id').replace('_', ' ').replace('_', ' ');
						$('body').attr('data-derection', direction);
						if ($('.section[data-id="' + nextIndex + '"]').find('.ppslide').hasClass('light_bg')) {
							$('body').removeClass('dark_bg').addClass('light_bg');
						} else {
							$('body').removeClass('light_bg').addClass('dark_bg');
						}
						setTimeout(function () {
							$('.section_number').html('0' + nextIndex);
							$('.page_title p').html(new_title);
						}, 650);

						if (!$('.section[data-id="' + nextIndex + '"]').find('.oi_ajax_port_holder').length && !$('.section[data-id="' + nextIndex + '"]').find('.wpb_revslider_element').length && !$('.section[data-id="' + nextIndex + '"]').find('.no_animation').length) {
							if (direction === 'up') {
								if (!$('.section[data-id="' + index + '"]').find('.oi_ajax_port_holder').length && !$('.section[data-id="' + index + '"]').find('.wpb_revslider_element').length && !$('.section[data-id="' + index + '"]').find('.no_animation').length) {
									$('.section[data-id="' + index + '"] >div >div >div >div').animate({
										opacity: 0,
										'padding-top': '200px'
									}, 700);
								}
								$('.section[data-id="' + nextIndex + '"] >div >div >div >div').css({
									'opacity': 0,
									'padding-bottom': '0px',
									'padding-top': '200px'
								});
							} else {
								$('.section[data-id="' + nextIndex + '"] >div >div >div >div').css({
									'opacity': 0,
									'padding-top': '0px',
									'padding-bottom': '200px'
								});
								if (!$('.section[data-id="' + index + '"]').find('.oi_ajax_port_holder').length && !$('.section[data-id="' + index + '"]').find('.wpb_revslider_element').length && !$('.section[data-id="' + index + '"]').find('.no_animation').length) {
									$('.section[data-id="' + index + '"] >div >div >div >div').animate({
										opacity: 0,
										'padding-bottom': '200px'
									}, 700);
								}
							}
							$('.section[data-id="' + nextIndex + '"] >div >div >div >div').animate({
								opacity: 1,
								'padding-top': '0px',
								'padding-bottom': '0px'
							}, 1600);
						}
					},
					afterLoad: function () {
						$('.hamburger_holder span').toggleClass('moving');
					},

					afterRender: function () {
						if ($('.active').find('.ppslide').hasClass('light_bg')) {
							$('body').addClass('light_bg');
						} else {
							$('body').addClass('dark_bg');
						}
					}

				});
				$("#pagepiling > .vc_row-full-width").remove();
			}
		});
	}

	if ($(window).width() < 768) {
		if ($('.oi_heading_icon').hasClass('oi_heading_icon_right')) {
			$('.oi_heading_icon').removeClass('oi_heading_icon_right').addClass('oi_heading_icon_left');
		}
	}

	$('.hamburger_holder span').each(function () {
		$(this).on("click", function () {
			$('body').toggleClass('go_overlay');
			if ($('body').hasClass('active_extra')) {
				$('body').removeClass('active_extra');
			}
			setTimeout(function () {
				$('body').toggleClass('active_menu');
				$('.hamburger_holder span').toggleClass('icon_menu icon_close');
				$('.hamburger_holder span').delay(300).animate({
					opacity: 1
				}, 150);
			}, 150);
			$('.hamburger_holder span').animate({
				opacity: 0
			}, 150);
		});
	});

	if ($('#range_slider').length) {
		var $range = $("#range_slider");

		$range.ionRangeSlider({
			type: "double",
			hide_min_max: true,
			hide_from_to: true,
		});

		$range.on("change", function () {
			var $this = $(this),
				from = $this.data("from"),
				to = $this.data("to");

			$('.price_label').find('.from').text('$' + from);
			$('.price_label').find('.to').text('$' + to);
		});
	}

	$('.call_extra').each(function () {
		$(this).on("click", function () {
			$('body').toggleClass('active_extra');
		});
	});

	if ($('#serviceSlide').length) {
		$('#serviceSlide').owlCarousel({
			autoplayTimeout: 5000,
			autoplay: true,
			nav: true,
			dots: false,
			loop: false,
			margin: 30,
			autoplayHoverPause: true,
			navText: ['<i class="fa fa-angle-left" aria-hidden="true"></i>', '<i class="fa fa-angle-right" aria-hidden="true"></i>'],
			responsive: {
				0: {
					items: 1
				},
				769: {
					items: 2

				},
				1025: {
					items: 3
				}
			}
		});
	}

	if ($('#customPortfolio').length) {
		var owl = $('#customPortfolio');
		owl.owlCarousel({
			autoplayTimeout: 5000,
			autoplay: false,
			nav: true,
			dots: false,
			loop: true,
			animateIn: 'fadeIn',
			animateOut: 'fadeOut',
			navContainer: '.pfolio-customNav',
			navElement: 'a class="oi_crea_a"',
			navText: ['<img width="28" alt="" src="framework/img/arr_l.png">', '<img width="28" alt="" src="framework/img/arr_r.png">'],
			margin: 0,
			autoplayHoverPause: false,
			items: 1
		});
	}

	if ($('#testimonialSlide').length) {
		$('#testimonialSlide').owlCarousel({
			autoplayTimeout: 5000,
			autoplay: true,
			nav: false,
			dots: false,
			loop: true,
			margin: 0,
			autoplayHoverPause: true,
			navText: ['&larr;', '&rarr;'],
			items: 1
		});
	}

	function timer() {
		var d = new Date();
		var min = d.getMinutes();
		var sec = d.getSeconds();
		var hr = d.getHours();
		if (hr < 10) {
			hr = "0" + hr;
		}
		if (d.getMinutes() < 10) {
			min = "0" + d.getMinutes();
		}
		if (d.getSeconds() < 10) {
			sec = "0" + d.getSeconds();
		}
		document.getElementById("timeclock").innerHTML = "" + hr + ":" + min + ":" + sec;

	}
	if ($('#timeclock').length) {
		setInterval(timer, 100);
	}


	$('.overlay').each(function () {
		$(this).on("click", function () {
			$('body').toggleClass('go_overlay');
			if ($('body').hasClass('active_extra')) {
				$('body').removeClass('active_extra');
			}
			setTimeout(function () {
				$('body').toggleClass('active_menu');
				$('.hamburger_holder span').toggleClass('icon_menu icon_close');
				$('.hamburger_holder span').delay(300).animate({
					opacity: 1
				}, 150);
			}, 150);
			$('.hamburger_holder span').animate({
				opacity: 0
			}, 150);
		});
	});


	$("body").on("click", ".send-form", function () {
		var thisis = $(this).parents('form');
		var name = thisis.find('.form-name').val();
		var subject = thisis.find('.form-subject').val();
		var email = thisis.find('.form-email').val();
		var message = thisis.find('.form-message').val();
		$.ajax({
			url: "framework/mailer.php",
			type: "post",
			dataType: "json",
			data: {
				"name": name,
				"subject": subject,
				"email": email,
				"message": message,
			},
			success: function (data) {
				var i = data.block;
				var msg = data.msg;
				if (i === 1) {
					thisis.find('.form-name').val('');
					thisis.find('.form-subject').val('');
					thisis.find('.form-email').val('');
					thisis.find('.form-message').val('');
				} else
				if (i === 2) {
					thisis.find('.wpcf7-response-output').addClass('wpcf7-validation-errors');
				}
				thisis.find('.wpcf7-response-output').html(msg).show('fast');
			}
		});
		event.preventDefault();
	});


	$('a[data-rel^=lightcase]').lightcase();
	$('.woocommerce-product-gallery__wrapper a').attr('data-rel', 'lightcase:gallery');
	$('.woocommerce-product-gallery__wrapper a').lightcase();
	lightcase.resize();
	if ($(window).width() > 900) {
		var win = 0;
		var winh = 0;
		$(window).load(function () {
			win = $(window).width();
			winh = $(window).height();
		});
		$(window).bind('resize', function () {
			if (window.RT) {
				clearTimeout(window.RT);
			}
			window.RT = setTimeout(function () {

				if ((Math.abs(win - $(window).width()) > 40) || (Math.abs(winh - $(window).height()) > 40)) {
					$('body').css('opacity', 0);
					this.location.reload(false);
				}

			}, 100);
		});
	}

	function initparticles() {
		bubbles();
	}


	function bubbles() {
		$.each($(".bubbles"), function () {
			var bubblecount = ($(this).width() / 30);
			for (var i = 0; i <= bubblecount; i++) {
				var size = ($.rnd(30, 60) / 10);
				$(this).append('<span class="particle" style="top:' + $.rnd(10, 90) + '%; left:' + $.rnd(0, 95) + '%;width:' + size + 'px; height:' + size + 'px;animation-delay: ' + ($.rnd(0, 30) * 0.1) + 's;"></span>');
			}
		});
	}


	jQuery.rnd = function (m, n) {
		m = parseInt(m);
		n = parseInt(n);
		return Math.floor(Math.random() * (n - m + 1)) + m;
	};

	initparticles();


	jQuery('<div class="quantity-nav"><div class="quantity-button quantity-up">+</div><div class="quantity-button quantity-down">-</div></div>').insertAfter('.quantity input');
	jQuery('.quantity').each(function () {
		var spinner = jQuery(this),
			input = spinner.find('input[type="number"]'),
			btnUp = spinner.find('.quantity-up'),
			btnDown = spinner.find('.quantity-down'),
			min = input.attr('min'),
			max = input.attr('max');

		btnUp.click(function () {
			var oldValue = parseFloat(input.val());
			var newVal;
			if (oldValue >= max) {
				newVal = oldValue;
			} else {
				newVal = oldValue + 1;
			}
			spinner.find("input").val(newVal);
			spinner.find("input").trigger("change");
		});

		btnDown.click(function () {
			var oldValue = parseFloat(input.val());
			var newVal;
			if (oldValue <= min) {
				newVal = oldValue;
			} else {
				newVal = oldValue - 1;
			}
			spinner.find("input").val(newVal);
			spinner.find("input").trigger("change");
		});

	});

	$(document).ready(function () {
		$('.oi_vc_button').each(function (index, element) {
			var oi_color = $(this).css("color");
			var oi_bg = $(this).css("background-color");
			var oi_border_color = $(this).css("borderTopColor");
			$(element).hover(
				function () {
					$(this).css({
						'color': $(this).attr('data-title-color-hover'),
						'background': $(this).attr('data-bg-color-hover'),
						'border-color': $(this).attr('data-border-c-hover'),
					});
				},
				function () {
					$(this).css({
						'color': oi_color,
						'background': oi_bg,
						'border-color': oi_border_color,
					});
				}
			);
		});

		$(".oi_custom_heading_holder").each(function () {
			if ($(this).height() > 40) {
				$(this).find(".oi_heading_icon:not(.oi_heading_icon_center)").css('margin-top', ($(this).height() - $(this).find('i').height()) / 2);
			} else {
				$(this).find(".oi_heading_icon:not(.oi_heading_icon_center)").css('margin-top', -2);
				$(this).find(".oi_heading_icon:not(.oi_heading_icon_center)").css('margin-right', 5);
			}
		});

		$(".oi_over").append('<div class="oi_overlay"></div>');


		$('.oi_owl_slider').each(function (index, element) {
			var id = $(element).attr('id');
			if ($('#' + id).attr('data-arrows') === 'true') {
				$('<i class="fa fa-angle-right"></i>').css('font-size', $(element).attr('data-icon-size')).appendTo($('#' + id + ' .owl-next'));
				$('<i class="fa fa-angle-left"></i>').css('font-size', $(element).attr('data-icon-size')).appendTo($('#' + id + ' .owl-prev'));
				var oi_color = $(this).attr('data-color');
				var oi_color_h = $(this).attr('data-color-hover');
				$('#' + id + ' .owl-nav i').hover(
					function () {
						$(this).css({
							'color': oi_color_h,
						});
					},
					function () {
						$(this).css({
							'color': oi_color
						});
					}
				);
			}
		});

		$('.oi_partner_holder').each(function (index, element) {
			var id = $(element).attr('id');
			$("#" + id).tipso({
				speed: 0,
				background: $("#" + id).attr('data-bg'),
				color: $("#" + id).attr('data-color'),
				position: $("#" + id).attr('data-position'),
				width: 0,
				maxWidth: "400",
				delay: 0,
				animationIn: "fadeIn",
				animationOut: "fadeOut",
				offsetX: 0,
				offsetY: 0,
				tooltipHover: false,
				content: null,
				ajaxContentUrl: null,
				useTitle: true,
				onBeforeShow: null,
				onShow: null,
				onHide: null
			});

		});

		$.fn.equalizeHeights = function () {
			return this.height(Math.max.apply(this, $(this).map(function (i, e) {
				return $(e).height();
			}).get()));
		};
		$('.oi_inner_equalize_heights .wpb_column').equalizeHeights();

	});
});
