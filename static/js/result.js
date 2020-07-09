
var play1, play2, play3, play4;

'use strict';
$(document).ready(function () {

	var result_img1 = document.getElementById('result_img1');
	var result_img2 = document.getElementById('result_img2');
	var result_img3 = document.getElementById('result_img3');
	var result_img4 = document.getElementById('result_img4');
	var cube1 = document.getElementById('cube1');
	var cube2 = document.getElementById('cube2');
	var cube3 = document.getElementById('cube3');
	var cube4 = document.getElementById('cube4');


	// $(cube1).click(function () {
	// 	$(result_img1).slideToggle();
	// })
	// $(cube2).click(function () {
	// 	$(result_img2).slideToggle();
	// })
	// $(cube3).click(function () {
	// 	$(result_img3).slideToggle();
	// })
	// $(cube4).click(function () {
	// 	$(result_img4).slideToggle();
	// })

	// function slideDown (result_img) {
	// 	if (result_img.style.display == 'none' || result_img.style.display == '' ) {
	// 		$(result_img).slideDown();
	// 	}
	// }


    var currentPage = 1;

    var audio1 = document.getElementById('music1');
    var audio2 = document.getElementById('music2');
    var audio3 = document.getElementById('music3');
    var audio4 = document.getElementById('music4');

    play1 = function p1() {
        if (audio1.paused) {
            console.log("play audio1");
            audio1.play();
            // document.getElementById('musBtn1');
        }else{
            console.log("pause audio1");

            audio1.pause();
            audio1.currentTime = 0;
            // document.getElementById('musBtn1');
        }
    }
    play2 = function p2() {
        if (audio2.paused) {
            console.log("play audio2");

            audio2.play();
            // document.getElementById('musBtn2');
        }else{
            console.log("pause audio2");

            audio2.pause();
            audio2.currentTime = 0;
            // document.getElementById('musBtn2');
        }
    }
    play3 = function p3() {
        if (audio3.paused) {
            console.log("play audio3");
            audio3.play();
            // document.getElementById('musBtn3');
        }else{
            console.log("pause audio3");
            audio3.pause();
            audio3.currentTime = 0;
            // document.getElementById('musBtn3');
        }
    }
    play4 = function p4() {
        if (audio4.paused) {
            console.log("play audio4");
            audio4.play();
            // document.getElementById('musBtn4');
        }else{
            console.log("pause audio4");
            audio4.pause();
            audio4.currentTime = 0;
            // document.getElementById('musBtn4');
        }
    }

    window.onload = function(){
        console.log("onload");
        play1();
		// slideDown(result_img1);
	}

    function onNavigate(){
        console.log(currentPage);
        currentPage = parseInt(currentPage);
        switch (currentPage){
            case 1:
				play1();
				// slideDown(result_img1);
                break;
            case 2:
                play2();
				// slideDown(result_img2);
				break;
            case 3:
                play3();
				// slideDown(result_img3);
				break;
            case 4:
                play4();
				// slideDown(result_img4);
				break;
		}
		
    }




	var $wrap = $(".wrapper"),
        pages = $(".page").length,
        scrolling = false,
        $navPanel = $(".nav-panel"),
        $scrollBtn = $(".scroll-btn"),
        $navBtn = $(".nav-btn");

	/*****************************
	***** NAVIGATE FUNCTIONS *****
	*****************************/
	function manageClasses() {
		$wrap.removeClass(function (index, css) {
			return (css.match(/(^|\s)active-page\S+/g) || []).join(' ');
		});
		$wrap.addClass("active-page" + currentPage);
		$navBtn.removeClass("active");
		$(".nav-btn.nav-page" + currentPage).addClass("active");
		$navPanel.addClass("invisible");
		scrolling = true;
		setTimeout(function () {
			$navPanel.removeClass("invisible");
			scrolling = false;
			onNavigate();
		}, 1000);
	}
	function navigateUp() {
		if (currentPage > 1) {
			currentPage--;
			if (Modernizr.csstransforms) {
				manageClasses();
			} else {
				$wrap.animate({ "top": "-" + ((currentPage - 1) * 100) + "%" }, 1000);
			}
		}
	}

	function navigateDown() {
		if (currentPage < pages) {
			currentPage++;
			if (Modernizr.csstransforms) {
				manageClasses();
			} else {
				$wrap.animate({ "top": "-" + ((currentPage - 1) * 100) + "%" }, 1000);
			}

		}
	}

	/*********************
	***** MOUSEWHEEL *****
	*********************/
	$(document).on("mousewheel DOMMouseScroll", function (e) {
		if (!scrolling) {
			if (e.originalEvent.wheelDelta > 0 || e.originalEvent.detail < 0) {
				navigateUp();
			} else {
				navigateDown();
			}
		}
	});

	/**************************
	***** RIGHT NAVIGATION ****
	**************************/

	/* NAV UP/DOWN BTN PAGE NAVIGATION */
	$(document).on("click", ".scroll-btn", function () {
		if ($(this).hasClass("up")) {
			navigateUp();
		} else {
			navigateDown();
		}
	});

	/* NAV CIRCLE DIRECT PAGE BTN */
	$(document).on("click", ".nav-btn", function () {
		if (!scrolling) {
			var target = $(this).attr("data-target");
			if (Modernizr.csstransforms) {
				$wrap.removeClass(function (index, css) {
					return (css.match(/(^|\s)active-page\S+/g) || []).join(' ');
				});
				$wrap.addClass("active-page" + target);
				$navBtn.removeClass("active");
				$(this).addClass("active");
				$navPanel.addClass("invisible");
				currentPage = target;
				scrolling = true;
				setTimeout(function () {
					$navPanel.removeClass("invisible");
					scrolling = false;

			        onNavigate();
				}, 1000);
			} else {
				$wrap.animate({ "top": "-" + ((target - 1) * 100) + "%" }, 1000);
			}

		}
	});

});