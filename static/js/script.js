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
        
        $(this).addClass("active");

        $(this).parent().siblings(".tab").find(".tab-link").removeClass("active");

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
});