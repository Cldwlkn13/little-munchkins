$(document).ready(function () {
    $(".sidenav").sidenav({ edge: "right" });

    $.get('static/text/countries.txt', function (data) {
        var lines = data.split('\n');
        $.each(lines, function (k, v) {
            var $newOpt = $("<option>").attr("value", v).text(v)
            $('#country').append($newOpt);
        });
    });

    $('select').formSelect();

    $('#show-recipe-card').on("click", function(){
        $('#sample-recipe-content').toggle();
    });

    function slideAndFadeIn(elem, animateLength, timeout) {
        setTimeout(function() {
            $(elem).animate({ opacity: 1 }, animateLength);
        }, timeout);
    }

    slideAndFadeIn("#home-info-text-1", 2000, 0);
    slideAndFadeIn("#home-info-text-2", 2000, 1500);
    slideAndFadeIn("#home-info-text-3", 2000, 3000);

    $('#ingredients-tab, #desc-tab, #method-tab').click(function(){        
        var selector = $(this).get(0).id.toString().replace("-tab","");
        $(this).addClass("active grey darken-3");
        $(this).parent().siblings(".tab").find(".tab-link").removeClass("active grey darken-3");
        var tabs = $(this).parent().parent().parent().next();
        var tab = tabs.children("#" + selector);
        tab.css("display", "block");
        tab.siblings().css("display", "none");
    });

    $("#sample-recipe-content").find("#desc-tab").click();

    $("#password_confirm").on("focusout", function () {
        if (!validatePassword()) {
            $(this).removeClass("valid").addClass("invalid");
            $("#lbl_password_confirm").text("Passwords do not match")
        } else {
            $(this).removeClass("invalid").addClass("valid");
            $("#lbl_password_confirm").text("Passwords match")
        }
    });

    $('#register-form').submit(function (e) {
        var bool = validatePassword();
        if (!bool){
            e.preventDefault();
            alert("Passwords do not match");
        }
        else
            return true; //continue to submit form
    });

    function validatePassword() {
        var password = $("#password").val();
        var confirmPassword = $("#password_confirm").val();
        if (password != confirmPassword) {
            return false;
        }
        else {
            return true;
        }
    }

    setTimeout(function() {
        $('.flashes').fadeOut('slow');
    }, 2000);

    $('#builder-add-step').click(function() {      
        var countsteps = $('.steps .step').length;
        console.log(countsteps)
        var i = countsteps + 1;

        var step = `<div class='row step' id='step-${i}'>` +
                        "<div class='input-field col m2'>" +
                            `<select id='step-${i}-type'>` +
                                "<option value='1' selected>Prepare</option>" +
                                "<option value='2'>Cook</option>" +
                            "</select>" +
                        "</div>" +
                        "<div class='input-field col m8'>" +
                            `<input type='text' id='step-${i}-desc' name='step-${i}-desc' minlength='1' maxlength='100' class='validate' required />` +
                            `<label for='step-${i}-desc'>Describe Step ${i}</label>` +
                        "</div>" +
                        "<div class='input-field col m2'>" +
                            `<input type='text' id='time-input-${i}' name='time-input-${i}'  minlength='1' maxlength='3' class='validate' pattern='^[0-9]{1,3}$' required />` +
                            `<label for='time-input-${i}'>Time</label>` +
                        "</div>" +
                    "</div>"    
        
        $('.steps').append(step); 

        $(`#step-${i}-type`).formSelect();
    });
});