$(document).ready(function () {
    //materialize init
    $(".sidenav").sidenav({ edge: "right" });
    $('.modal').modal();
    $('select').formSelect();
    $('.collapsible').collapsible();

    //events
    //register
    $('#username').change(function(){
        loadCountryOptions($('#country'));
    });

    $("#password_confirm").on("focusout", function () {
        if (!validatePassword()) {
            $(this).removeClass("valid").addClass("invalid");
            $("#lbl_password_confirm").text("Passwords do not match");
        } else {
            $(this).removeClass("invalid").addClass("valid");
            $("#lbl_password_confirm").text("Passwords match");
        }
    });

    $('#register-form').submit(function (e) {
        var bool = validatePassword();
        if (!bool){
            e.preventDefault();
            alert("Passwords do not match");
        }
        else
            return true;
    });


    $('#user-edit').click(function(){
        $(this).siblings('form').first().children('input').prop("disabled", false);
        $(this).siblings('form').first().children('select').prop("disabled", false);
        $('.profile-submit-btn').show();
        $(this).hide();
        loadCountryOptions($('#country'));
    });

    $('.profile-submit-btn').click(function(){
        var usernametest = testRegex($('.profile-submit-btn').siblings('input[name="username"]'));
        var emailtest = testRegex($('.profile-submit-btn').siblings('input[name="email"]'));
        var fnametest = testRegex($('.profile-submit-btn').siblings('input[name="first_name"]'));
        var lnametest = testRegex($('.profile-submit-btn').siblings('input[name="first_name"]'));

        if(usernametest && emailtest && fnametest && lnametest){
            $('#user-edit').show();
        }
    });

    //recipe card
    $('.add-favourite').click(function(event){
        event.preventDefault();
        var myelem = $(this);
        var data = {'data': $(this).siblings('input[name="_id"]').attr("value") };
        $.ajax({
            type: "POST",
            data: data,
            url: "/recipe/favourite",
            success: function(response){   
                isFavourite = $.parseJSON(response.toLowerCase());
                if(isFavourite){
                    $(myelem).removeClass("purple").addClass("light-green");
                    $(myelem).siblings('span').first().text('Remove Favourite');
                }
                else {
                    $(myelem).removeClass("light-green").addClass("purple");
                    $(myelem).siblings('span').first().text('Favourite this recipe');
                }
            }
        });

        if($('#profile-wrap').is(":visible")){
            refreshProfile();
        }
    });

    $('.ingredients-tab, .desc-tab, .method-tab').click(function(){        
        var selector = $(this).prop('className').split(' ')[0].replace("-tab", "");
        $(this).addClass("active grey darken-3");
        $(this).parent().siblings(".tab").find(".tab-link").removeClass("active grey darken-3");
        var tabs = $(this).parent().parent().parent().next();
        var tab = tabs.children("." + selector + "-content");
        tab.css("display", "block");
        tab.siblings().css("display", "none");
    });

    $('.expand-content').click(function(){
        if($(this).hasClass('expanded')) {
            $(this).siblings('span').first().text("Click to see more");
            $(this).children('i').first().text("expand_more");
            $(this).parent().parent().siblings('.card-content').children(".recipe-img-header").css("display", "block");
            $(this).parent().parent().siblings('.prep-time').css("display", "none");
            $(this).parent().parent().siblings('.recipe-img-wrapper').css("display", "none");
            $(this).parent().parent().siblings('.card-tabs').css("display", "none");
            $(this).parent().parent().siblings('.card-tab-content').css("display", "none");
            $(this).removeClass('expanded');
            return;
        }
        $(this).siblings('span').first().text("Click to see less");
        $(this).children('i').first().text("expand_less");
        $(this).parent().parent().siblings('.card-content').children(".recipe-img-header").css("display", "none");
        $(this).parent().parent().siblings('.prep-time').css("display", "block");
        $(this).parent().parent().siblings('.recipe-img-wrapper').css("display", "block");
        $(this).parent().parent().siblings('.card-tabs').css("display", "block");
        $(this).parent().parent().siblings('.card-tab-content').css("display", "block");
        $(this).parent().parent().siblings('.card-tab-content').children('.desc-content').first().css("display", "block");
        $(this).addClass('expanded');
    });

    //recipe builder
    $('#preview-recipe-card').on("click", function(){
        $('#preview-recipe-content').toggle();
    });

    $('#builder-add-step').click(function() {      
        var countsteps = $('.steps .step').length;
        var i = countsteps + 1;
        var step = `<div class='row step cyan lighten-4' id='step-${i}'>` +
                        "<div class='input-field col m2'>" +
                            `<select id='step-${i}-type' name='step-${i}-type'>` +
                                "<option value='prepare' selected>Prepare</option>" +
                                "<option value='cook'>Cook</option>" +
                            "</select>" +
                            `<label for="step-${i}-type">Action Type</label>` +
                        "</div>" +
                        "<div class='input-field col m7'>" +
                            `<input type='text' id='step-${i}-desc' name='step-${i}-desc' minlength='1' maxlength='100' class='validate' required />` +
                            `<label for='step-${i}-desc'>Action</label>` +
                        "</div>" +
                        "<div class='input-field col m2'>" +
                            `<input type='text' id='step-${i}-time' name='step-${i}-time'  minlength='1' maxlength='3' class='validate' pattern='^[0-9]{1,3}$' required />` +
                            `<label for='step-${i}-time'>Time (mins)</label>` +
                        "</div>" +
                        "<div class='input-field col m1'>" +
                            `<a href="#" id='remove-step-${i}'><i class="material-icons black-text">delete</i></a>` + 
                        "</div>" +
                    "</div>";
      
        $('.steps').append(step); 
        $(`#step-${i}-type`).formSelect();
        $(`#remove-step-${i}`).on('click',function(){
            if(confirm("Are you sure?")) {
                $(`#step-${i}`).hide();
                $(`#step-${i}`).children().find('input').attr("disabled", true);
            }
        });
    });

    $('#builder-add-ingredient').click(function() {      
        var countingredients = $('.ingredients .ingredient').length;
        var i = countingredients + 1;
        var ingredient = `<div class='row ingredient cyan lighten-4' id='ingredient-${i}'>` +
                            "<div class='input-field col m8'>" +
                                `<input type='text' id='ingredient-${i}-desc' name='ingredient-${i}-desc' minlength='1' maxlength='30' class='validate' required />` +
                                `<label for='ingredient-${i}-desc'>Ingredient</label>` +
                            "</div>" +
                            "<div class='input-field col m2'>" +
                                `<input type='text' id='ingredient-${i}-measure' name='ingredient-${i}-measure'  minlength='1' maxlength='4' class='validate' pattern='^[0-9]{1,4}$' required />` +
                                `<label for='ingredient-${i}-measure'>Measure</label>` +
                            "</div>" +
                            "<div class='input-field col m1'>" +
                                `<input type='text' id='ingredient-${i}-unit' name='ingredient-${i}-unit'  maxlength='8' class='validate' pattern='^[a-z]{,8}$' />` +
                                `<label for='ingredient-${i}-unit'>Unit</label>` +
                            "</div>" +
                            "<div class='input-field col m1'>" +
                                `<a href="#" id='remove-ingredient-${i}'><i class="material-icons black-text">delete</i></a>` + 
                            "</div>" +
                        "</div>";    
      
        $('.ingredients').append(ingredient); 
        $(`#remove-ingredient-${i}`).on('click',function(){
            if(confirm("Are you sure?")) {
                $(`#ingredient-${i}`).hide();
                $(`#ingredient-${i}`).children().find('input').attr("disabled", true);
            }
        });
    });

    $('#preview-recipe').click(function(){
        $('#builder-form').attr("target", "_blank");
    });

    $('.submit-builder').click(function(){
        $('#builder-form').attr("target", "");
        $('#editor-form').attr("target", "");
    });


    // editor
    $(`.remove-step`).on('click',function(){
        if(confirm("Are you sure?")) {
            var i = $(this).get(0).id.split('-')[2];
            $(`#step-${i}`).hide();
            $(`#step-${i}`).children().find('input').attr("disabled", true);
            $(`#step-${i}`).children().find('select').attr("disabled", true);
        }
    });

    $(`.remove-ingredient`).on('click',function(){
        if(confirm("Are you sure?")) {
            var i = $(this).get(0).id.split('-')[2];
            $(`#ingredient-${i}`).hide();
            $(`#ingredient-${i}`).children().find('input').attr("disabled", true);
        }
    });

    $('#preview-recipe').click(function(){
        $('#editor-form').attr("target", "_blank");
    });

    $('#delete-recipe').click(function(){
        $('#editor-form').attr("target", "");
    });

    $('#cancel-changes').click(function(){
        $('#editor-form').attr("target", "");
    });

    //functions
    function loadCountryOptions(elem){
        $.get('/static/text/countries.txt', function (data) {
            var lines = data.split('\n');
            $.each(lines, function (k, v) {
                var $newOpt = $("<option>").attr("value", v).text(v);
                elem.append($newOpt);
             });
        });
    }

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

    function refreshProfile() {
        var username = $('input[name="username"]');
        var isDisabled = username.attr('disabled') == "disabled";
        var url = "/profile/" + username.attr("value");
        if(isDisabled){
            $.ajax({
                type: "GET",
                url: url,
                success:function(response){ 
                    window.location.reload();
                }
            });
        }
    }

    function slideAndFadeIn(elem, animateLength, timeout) {
        setTimeout(function() {
            $(elem).animate({ opacity: 1 }, animateLength);
        }, timeout);
    }

    function testRegex(elem){
        var regex = new RegExp(elem.attr("pattern"), 'g');
        return regex.test(elem.val())
    }

    //method calls
    slideAndFadeIn("#home-info-text-1", 2000, 0);
    slideAndFadeIn("#home-info-text-2", 2000, 1500);
    slideAndFadeIn("#home-info-text-3", 2000, 3000);

    setTimeout(function() {
        $('.flashes').fadeOut('slow');
    }, 2000);
});