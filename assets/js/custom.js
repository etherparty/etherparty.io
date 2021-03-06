// Javascript Document

/* =================================
   LOADER                     
=================================== */
// makes sure the whole site is loaded
$(window).load(function() {

    "use strict";

    // will first fade out the loading animation
    $(".signal").fadeOut();
        // will fade out the whole DIV that covers the website.
    $(".preloader").fadeOut("slow");

});


/* =================================
   LOGIN-SIGNUP MODAL                     
=================================== */

function showRegisterForm(){
    "use strict";
    $('.loginBox').fadeOut('fast',function(){
        $('.registerBox').fadeIn('fast');
        $('.login-footer').fadeOut('fast',function(){
            $('.register-footer').fadeIn('fast');
        });
        $('.modal-title').html('Create an Account');
        $('.modal-subtitle').html('Sign up to Etherparty Beta');
    });
    $('.error').removeClass('alert alert-danger').html('');
}


function showLoginForm(){
    "use strict";
    $('#loginModal .registerBox').fadeOut('fast',function(){
        $('.loginBox').fadeIn('fast');
        $('.register-footer').fadeOut('fast',function(){
            $('.login-footer').fadeIn('fast');
        });
        
        //$('.modal-title').html('Sign in to <span>Etherparty</span>');
        //$('.modal-subtitle').html('Enter your email and password');
    });
    $('.error').removeClass('alert alert-danger').html('');
}


function openLoginModal(){
    "use strict";
    showLoginForm();
    $('#loginModal').modal('show');
}

function openPrivModal(){
    "use strict";
    //showLoginForm();
    $('#privModal').modal('show');
}

function openRegisterModal(){
    "use strict";
    showRegisterForm();
    $('#loginModal').modal('show');
}


/* =================================
   EARLY ACCESS MODAL                     
=================================== */
function showEarlyAccessForm(){
    "use strict";
    $('.modal-title').html('Get Early Access');
    $('.modal-subtitle').html('Enter your email and Join Beta.');
    
    $('.error').removeClass('alert alert-danger').html('');
}

function openEarlyAccessModal(){
    "use strict";
    showEarlyAccessForm();
    $('#loginModal').modal('show');
}


/* =================================
   SCROLL NAVBAR
=================================== */
$(window).scroll(function(){
    "use strict";
    var b = $(window).scrollTop();
    if( b > 60 ){
        $(".navbar").addClass("is-scrolling");
    } else {
        $(".navbar").removeClass("is-scrolling");
    }
});


/* =================================
   TYPING EFFECT
=================================== */
(function($) {

    "use strict";

    $('[data-typer-targets]').typer();
    $.typer.options.clearOnHighlight=false;

})(jQuery);


/* =================================
   DATA SPY FOR ACTIVE SECTION                 
=================================== */
(function($) {
    
    "use strict";
    
    $('body').attr('data-spy', 'scroll').attr('data-target', '.navbar-fixed-top').attr('data-offset', '11');

})(jQuery);


/* =================================
   HIDE MOBILE MENU AFTER CLICKING 
=================================== */
(function($) {
    
    "use strict";
    
    $('.nav.navbar-nav li a').click(function () {
        var $togglebtn = $(".navbar-toggle");
        if (!($togglebtn.hasClass("collapsed")) && ($togglebtn.is(":visible"))){
            $(".navbar-toggle").trigger("click");
        }
    });

})(jQuery);


/* ==================================================== */
/* ==================================================== */
/* =======================================================
   DOCUMENT READY
======================================================= */
/* ==================================================== */
/* ==================================================== */

$(document).ready(function() {


"use strict";


/* =====================================
    PARALLAX STELLAR WITH MOBILE FIXES                    
======================================== */
if (Modernizr.touch && ($('.header').attr('data-stellar-background-ratio') !== undefined)) {
    $('.header').css('background-attachment', 'scroll');
    $('.header').removeAttr('data-stellar-background-ratio');
} else {
    $(window).stellar({
        horizontalScrolling: false
    });
}

/* =================================
    WOW ANIMATIONS                   
=================================== */
new WOW().init();

/* ==========================================
    EASY TABS
============================================= */
$('.tabs.testimonials').easytabs({
    animationSpeed: 300,
    updateHash: false,
    cycle: 10000
});

$('.tabs.features').easytabs({
    animationSpeed: 300,
    updateHash: false
});


/* ==========================================
   OWL CAROUSEL 
============================================= */
/* App Screenshot Carousel in Mobile-Download Section */
$("#owl-carousel-shots-phone").owlCarousel({
    singleItem:true,navigation: true,
    navigationText: [
        "<i class='icon arrow_carrot-left'></i>",
        "<i class='icon arrow_carrot-right'></i>"
                    ],
    addClassActive : true,
    itemsDesktop : [1200, 1],
    itemsDesktopSmall : [960, 1],
    itemsTablet : [769, 1],
    itemsMobile : [700, 1],
    responsiveBaseWidth : ".shot-container",
    items : 1,
    slideSpeed : 1000,
    mouseDrag : true,
    responsiveRefreshRate : 200,
    autoPlay: 5000
});

/* ==========================================
    VENOBOX - LIGHTBOX FOR GALLERY AND VIDEOS
============================================= */
$('.venobox').venobox();

/* ===================================================================
    fuck TWEETIE -  TWITTER FEED PLUGIN THAT WORKS WITH NEW Twitter 1.1 API
==================================================================== */
$.ajax({
    type: "GET",
    url: "tweets",
    success: function(d) {
        var linking = function (tweet) {
            var twit = tweet.replace(/(https?:\/\/([-\w\.]+)+(:\d+)?(\/([\w\/_\.]*(\?\S+)?)?)?)/ig,'<a href="$1" target="_blank" title="Visit this link">$1</a>')
                 .replace(/#([a-zA-Z0-9_]+)/g,'<a href="https://twitter.com/search?q=%23$1&amp;src=hash" target="_blank" title="Search for #$1">#$1</a>')
                 .replace(/@([a-zA-Z0-9_]+)/g,'<a href="https://twitter.com/$1" target="_blank" title="$1 on Twitter">@$1</a>');

            return twit;
        };

      d=JSON.parse(d);
      //console.log(d);
      var text = '';
      d.forEach(function(e) { text +=  '<li>' + linking(e[0]) + ' - <span class="date">' + e[1] + '</span></li>'});
      $('.subtweet').html(text);
    },
    error: function() {
      $('.subtweet').html('<div> loading tweets failed... </div>');
    } 
});



/* =================================
   SCROLL TO                  
=================================== */
var onMobile;

onMobile = false;
if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) { onMobile = true; }

if (onMobile === true) {
    jQuery('a.scrollto').click(function (event) {
    jQuery('html, body').scrollTo(this.hash, this.hash, {gap: {y: -10}, animation:  {easing: 'easeInOutCubic', duration: 0}});
    event.preventDefault();
});
} else {
    jQuery('a.scrollto').click(function (event) {
    jQuery('html, body').scrollTo(this.hash, this.hash, {gap: {y: -10}, animation:  {easing: 'easeInOutCubic', duration: 1500}});
        event.preventDefault();
});
}


/* ==========================================
   MAILCHIMP NEWSLETTER SUBSCRIPTION
============================================= */
$(".mailchimp-subscribe").ajaxChimp({
    callback: mailchimpCallback,
    url: "http://vanbex.us9.list-manage.com/subscribe/post?u=f4b29d37a4569bcfe566bd4d5&amp;id=db50508772" // Replace your mailchimp post url inside double quote "".  
});

function mailchimpCallback(resp) {
if(resp.result === 'success') {
    $('.mc-success')
    .html('<i class="icon icon_check_alt2"></i>' + resp.msg)
    .fadeIn(1000);

    $('.mc-failed').fadeOut(500);
        
} else if(resp.result === 'error') {
    $('.mc-failed')
    .html('<i class="icon icon_close_alt2"></i>' + resp.msg)
    .fadeIn(1000);
            
    $('.mc-success').fadeOut(500);
}
}

/* ==========================================
   FUNCTION FOR EMAIL ADDRESS VALIDATION
============================================= */
function isValidEmail(emailAddress) {

    var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);

    return pattern.test(emailAddress);

}

/* ==========================================
   LOCAL NEWSLETTER/EARLY ACCESS SUBSCRIPTION
============================================= */
$("#subscribe").submit(function(e) {
    e.preventDefault();
    var data = {
        email: $("#s-email").val()
    };

    if ( isValidEmail(data['email']) ) {
        $.ajax({
            type: "POST",
            url: "assets/php/subscribe.php",
            data: data,
            success: function() {
                $('.subscription-success').fadeIn(1000);
                $('.subscription-failed').fadeOut(500);
            }
        });
    } else {
        $('.subscription-failed').fadeIn(1000);
        $('.subscription-success').fadeOut(500);
    }

    return false;
});

/* =====================================================================
   LOGIN-MODAL VALIDATION. FIELD VALUES WILL BE SENT TO LOGIN-MODAL.PHP
======================================================================== */
$("#login-modal").submit(function(e) {
    e.preventDefault();
    var data = {
        email: $("#lm-email").val(),
        name: $("#lm-name").val(),
        alias: $("#lm-alias").val()
    };

    $("#lm-submit").attr('style','color:white');
    window.etherparty_timer = 0;
    $('#lm-submit').text("Registering, one moment ");
    window.etherparty_timer = setInterval(function() { 
      $("#lm-submit").append(" . "); timer += 1000; if (timer % 3000 == 0) $("#lm-submit").text('registering, one moment '); 
    }, 1000);
    $('#lm-submit').addClass('disabled');

    //if ( isValidEmail(data['email']) &&  ) { validation here
        $.ajax({
            type: "POST",
            url: "execute",
            data: data,
            success: function(d) {
              $('.lm-success').fadeIn(1000);
              $('.lm-failed').fadeOut(500);

              $('.lm-success-id').text(d);

              $('#lm-submit').text("Registration success!");

              getAndSaveUsers();

            },
            error: function() {
              $('.lm-failed').fadeIn(1000);
              $('.lm-success').fadeOut(500);

              $('#lm-submit').removeClass('disabled');
              $('#lm-submit').text("Submit Registration");
            }, 
            complete: function() {  clearInterval(window.etherparty_timer); }
        });
    //} else {
    //    $('.lm-failed').fadeIn(1000);
    //   $('.lm-success').fadeOut(500);
    //}

    return false;
});


/* ========================================================================================
   SIGNUP-MODAL VALIDATION. WITH CONFIRM PSW. FIELD VALUES WILL BE SENT TO SIGNUP-MODAL.PHP
=========================================================================================== */
$("#signup-modal").submit(function(e) {
    e.preventDefault();
    var data = {
        password: $("#sm-password").val(),
        email: $("#sm-email").val(),
        pswconfirm: $("#sm-confirm").val()
    };

    if ( isValidEmail(data['email']) && (data['password'].length > 1) && (data['password'].match(data['pswconfirm'])) ) {
        $.ajax({
            type: "POST",
            url: "assets/php/subscribe.php",
            data: data,
            success: function() {
                $('.sm-success').fadeIn(1000);
                $('.sm-failed').fadeOut(500);
            }
        });
    } else {
        $('.sm-failed').fadeIn(1000);
        $('.sm-success').fadeOut(500);
    }

    return false;
});

/* ==========================================
   EARLY ACCESS MODAL VALIDATION
============================================= */
$("#earlyaccess-modal").submit(function(e) {
    e.preventDefault();
    var data = {
        email: $("#lm-email").val()
    };

    if ( isValidEmail(data['email']) ) {
        $.ajax({
            type: "POST",
            url: "assets/php/subscribe.php",
            data: data,
            success: function() {
                $('.lm-success').fadeIn(1000);
                $('.lm-failed').fadeOut(500);
            }
        });
    } else {
        $('.lm-failed').fadeIn(1000);
        $('.lm-success').fadeOut(500);
    }

    return false;
});

/* ========================================================================================
   SIGNUP-DIVIDER VALIDATION. WITHOUT CONFIRM PSW. FIELD VALUES WILL BE SENT TO SIGNUP.PHP
=========================================================================================== */
$("#signup-divider").submit(function(e) {
    e.preventDefault();
    var data = {
        email: $("#signup-email").val(),
        password: $("#signup-password").val()
    };

    if ( isValidEmail(data['email']) && (data['password'].length > 1)) {
        $.ajax({
            type: "POST",
            url: "assets/php/subscribe.php",
            data: data,
            success: function() {
                $('.signup-success').fadeIn(1000);
                $('.signup-failed').fadeOut(0);
            }
        });
    } else {
        $('.signup-failed').fadeIn(1000);
        $('.signup-success').fadeOut(500);
    }

    return false;
});

/* ========================================================================================
   FAST-REGISTRATION VALIDATION. WITHOUT CONFIRM PSW. FIELD VALUES WILL BE SENT TO SIGNUP.PHP
=========================================================================================== */
$("#fast-reg").submit(function(e) {
    e.preventDefault();
    var data = {
        name: $("#fast-name").val(),
        email: $("#fast-email").val(),
        password: $("#fast-password").val()
    };

    if ( isValidEmail(data['email']) && (data['password'].length > 1) && (data['name'].length > 1) ) {
        $.ajax({
            type: "POST",
            url: "assets/php/subscribe.php",
            data: data,
            success: function() {
                $('.fast-success').fadeIn(1000);
                $('.fast-failed').fadeOut(500);
            }
        });
    } else {
        $('.fast-failed').fadeIn(1000);
        $('.fast-success').fadeOut(500);
    }

    return false;
});

/* =======================================================================
   DOUGHNUT CHART
========================================================================== */
var isdonut = 0;
        
$('.start-charts').waypoint(function(direction){
    if (isdonut == 1){}
        else {
            var doughnutData = [
                {
                    value: 50,
                    color:"#C0392B",
                    highlight: "#EA402F",
                    label: "Ethereum"
                },
                {
                    value: 25,
                    color: "#323A45",
                    highlight: "#4C5B70",
                    label: "Bitcoin"
                },
                {
                    value: 15,
                    color: "#949FB1",
                    highlight: "#A8B3C5",
                    label: "Storj"
                },
                {
                    value: 5,
                    color: "#27AE60",
                    highlight: "#29C36A",
                    label: "Fun"
                }

            ];

            var doughnut2Data = [
                {
                    value: 25,
                    color:"#C0392B",
                    highlight: "#EA402F",
                    label: "Smart Templates"
                },
                {
                    value: 49,
                    color: "#323A45",
                    highlight: "#4C5B70",
                    label: "Contracts as a Service"
                },
                {
                    value: 13,
                    color: "#2980B9",
                    highlight: "#2F97DC",
                    label: "Smart Monitors"
                },
                {
                    value: 12,
                    color: "#949FB1",
                    highlight: "#A8B3C5",
                    label: "Smart Storage"
                }
            ];

            
            
            var ctx = document.getElementById("chart-area").getContext("2d");
            window.myDoughnut = new Chart(ctx).Doughnut(doughnutData, {responsive : false});

            var ctx = document.getElementById("chart2-area").getContext("2d");
            window.myDoughnut = new Chart(ctx).Doughnut(doughnut2Data, {responsive : false});

            isdonut = 1;
        }
});

/* =======================================================================
   LINE CHART
========================================================================== */
var isline = 0;
        
$('.start-line').waypoint(function(direction){
    if (isline == 1){}
        else {

            var lineChartData = {
                labels : ["Jan 2015","June 2015","Dec 2015","Jan 2016","June 2016","Dec 2016","2017"],
                datasets : [
                    {
                        label: "Cryptocurrency adoption",
                        fillColor : "rgba(192,57,43,0.2)",
                        strokeColor : "rgba(192,57,43,1)",
                        pointColor : "rgba(192,57,43,1)",
                        pointStrokeColor : "#fff",
                        pointHighlightFill : "#fff",
                        pointHighlightStroke : "rgba(192,57,43,1)",
                        data : [10,20,20,25,30,37,45]
                    },
                    {
                        label: "Smart Contract adoption",
                        fillColor : "rgba(50,58,69,0.2)",
                        strokeColor : "rgba(50,58,69,1)",
                        pointColor : "rgba(50,58,69,1)",
                        pointStrokeColor : "#fff",
                        pointHighlightFill : "#fff",
                        pointHighlightStroke : "rgba(50,58,69,1)",
                        data : [10,23,33,57,74,81,96]
                    }
                ]

            };

            var ctx = document.getElementById("line-canvas").getContext("2d");
            window.myLine = new Chart(ctx).Line(lineChartData, {responsive: true});

            isline = 1;
        }
});

/* =======================================================================
   SIGNUP-DIVIDER ANIMATED POLYGON BACKGROUND
========================================================================== */
    var container = document.getElementById('canvas-bg');
    var renderer = new FSS.CanvasRenderer();
    var scene = new FSS.Scene();
    var light = new FSS.Light('323A45', '323A45');
    var geometry = new FSS.Plane(2000, 1000, 15, 8);
    var material = new FSS.Material('FFFFFF', 'FFFFFF');
    var mesh = new FSS.Mesh(geometry, material);
    var now, start = Date.now();

    function initialise() {
      scene.add(mesh);
      scene.add(light);
      container.appendChild(renderer.element);
      window.addEventListener('resize', resize);
    }

    function resize() {
      renderer.setSize(container.offsetWidth, container.offsetHeight);
    }

    function animate() {
      now = Date.now() - start;
      light.setPosition(300*Math.sin(now*0.001), 200*Math.cos(now*0.0005), 60);
      renderer.render(scene);
      requestAnimationFrame(animate);
    }

    initialise();
    resize();
    animate();


/* =======================================================================
   TIMECIRCLE - COUNTDOWN
========================================================================== */
var countdown =  $('.countdown-time');

createTimeCicles();

$(window).on('resize', windowSize);

function windowSize(){
    countdown.TimeCircles().destroy();
    createTimeCicles();
    countdown.on('webkitAnimationEnd mozAnimationEnd oAnimationEnd animationEnd', function() {
            countdown.removeClass('animated bounceIn');
    });
}

function createTimeCicles() {
    countdown.addClass('animated bounceIn');
    countdown.TimeCircles({
    fg_width: 0.011,
    bg_width: 0.1,
    circle_bg_color: '#ffffff',
    time: {
            Days: {color: '#c0392b'},
            Hours: {color: '#c0392b'},
            Minutes: {color: '#c0392b'},
            Seconds: {color: '#c0392b'}
           }
    });
    countdown.on('webkitAnimationEnd mozAnimationEnd oAnimationEnd animationEnd', function() {
    countdown.removeClass('animated bounceIn');
    });
}


/* ===========================================================
   BOOTSTRAP FIX FOR IE10 in Windows 8 and Windows Phone 8  
============================================================== */
if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
    var msViewportStyle = document.createElement('style');
    msViewportStyle.appendChild(
        document.createTextNode(
            '@-ms-viewport{width:auto!important}'
            )
        );
    document.querySelector('head').appendChild(msViewportStyle);
}

///////////////////////////////////////////////////////////////////////
// our custom fucking code
//
    function getAndSaveUsers() {
      //console.log("Called getAndSaveUsers");
      $.ajax({
          type: "GET",
          url: "users",
          success: function(d) {
              var temp = "";
              window.etherparty = JSON.parse(d); d = JSON.parse(d);
              d=d.slice(d.length - 5, d.length);
              //console.log(typeof d, d.length - 5, d.length, d.slice(d.length - 5, d.length) );
              
              d.forEach(function(e) {
                temp += "<tr> <th scope='row'>" + (e[0] + '') + "</th> <td>" + e[2] + " </td> <td> " + e[1] + "</td> <td> " + (new Date( +(e[3] + "000") )).toDateString() + "</tr>";
              });
              $('#reg-table').html(temp);
          }
      });
   }

   getAndSaveUsers();

   $( "#registrant-search" ).on('input', function() {
      //console.log('ran');
      var searchval = $("#registrant-search").val();
      var tempData = window.etherparty;
      //$(".search-results").text('searched ' + searchval );// Check input( $( this ).val() ) for validity here
      if( tempData ) {
        var temp = '';
        var maxLimit = 5;
        var count = 0;
        tempData.forEach(function(e) {
          //more logic here TODO
          var piece1 = ('' + e[0]).slice(0,searchval.length);
          var piece2 = ('' + e[2]).slice(0,searchval.length);

          if ( (searchval == piece1 || searchval == piece2) && count < 5) {
            temp += "<tr> <th scope='row'>" + e[0] + "</th> <td>" + e[2] + " </td> <td> " + e[1].slice(0,20) + "..." + "</td> <td> " + (new Date( +(e[3] + "000") )).toDateString() + "</tr>";

            count++;
          }
          //console.log(piece1, piece2, searchval, searchval == piece1, searchval == piece2, temp);
        });
        $("#reg-table-searched").html(temp);
      }
   });
   
   setTimeout(function(){ $("#registrant-search").trigger('input'); }, 3000);

});

