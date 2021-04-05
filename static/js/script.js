$(document).ready(function () {
    $(".sidenav").sidenav({ edge: "right" });
    $('.modal').modal();

    $('#username').change(function(){
        $.get('static/text/countries.txt', function (data) {
            var lines = data.split('\n');
            $.each(lines, function (k, v) {
                var $newOpt = $("<option>").attr("value", v).text(v)
                $('#country').append($newOpt);
            });
        });
    });

    $('.add-favourite').click(function(event){
        event.preventDefault();
        var myelem = $(this)
        var data = {'data': $(this).siblings('#favourite_id').attr("value") };
        $.ajax({
            type: "POST",
            data: data,
            url: "/favouriterecipe",
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
    });

    function renderIsFavourite(element){
        console.log(element)
    };

    $('select').formSelect();

    $('#preview-recipe-card').on("click", function(){
        $('#preview-recipe-content').toggle();
    });

    function slideAndFadeIn(elem, animateLength, timeout) {
        setTimeout(function() {
            $(elem).animate({ opacity: 1 }, animateLength);
        }, timeout);
    }

    slideAndFadeIn("#home-info-text-1", 2000, 0);
    slideAndFadeIn("#home-info-text-2", 2000, 1500);
    slideAndFadeIn("#home-info-text-3", 2000, 3000);

    $('.ingredients-tab, .desc-tab, .method-tab').click(function(){        
        var selector = $(this).prop('className').split(' ')[0].replace("-tab", "");
        console.log(selector);
        $(this).addClass("active grey darken-3");
        $(this).parent().siblings(".tab").find(".tab-link").removeClass("active grey darken-3");
        var tabs = $(this).parent().parent().parent().next();
        var tab = tabs.children("." + selector + "-content");
        tab.css("display", "block");
        tab.siblings().css("display", "none");
    });

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
            return true;
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
                            `<input type='text' id='step-${i}-time' name='step-${i}-time'  minlength='1' maxlength='3' class='validate' pattern='^[0-9.]{1,3}$' required />` +
                            `<label for='step-${i}-time'>Time (mins)</label>` +
                        "</div>" +
                        "<div class='input-field col m1'>" +
                            `<a href="#" id='remove-step-${i}'><i class="material-icons black-text">delete</i></a>` + 
                        "</div>" +
                    "</div>"    
      
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
                                `<input type='text' id='ingredient-${i}-unit' name='ingredient-${i}-unit'  minlength='1' maxlength='8' class='validate' pattern='^[a-z]{1,8}$' required />` +
                                `<label for='ingredient-${i}-unit'>Unit</label>` +
                            "</div>" +
                            "<div class='input-field col m1'>" +
                                `<a href="#" id='remove-ingredient-${i}'><i class="material-icons black-text">delete</i></a>` + 
                            "</div>" +
                        "</div>"    
      
        $('.ingredients').append(ingredient); 
        $(`#remove-ingredient-${i}`).on('click',function(){
            if(confirm("Are you sure?")) {
                $(`#ingredient-${i}`).hide();
                $(`#ingredient-${i}`).children().find('input').attr("disabled", true);
            }
        });
    });

    $('#preview-recipe').click(function(){
        $('#builder-form').attr("target", "_blank")
    });

    $('#submit-builder').click(function(){
        $('#builder-form').attr("target", "")
    });

    $('#user-edit').click(function(){
        $(this).siblings('form').first().children('input').prop("disabled", false);
        $('.profile-submit-btn').show();
        $(this).hide();
    });

    $('.profile-submit-btn').click(function(){
        $('#user-edit').show();
        $('.profile-submit-btn').hide();
    });

    $(`.remove-step`).on('click',function(){
        if(confirm("Are you sure?")) {
            var i = $(this).get(0).id.split('-')[2]
            $(`#step-${i}`).hide();
                $(`#step-${i}`).children().find('input').attr("disabled", true);
        }
    });

    $(`.remove-ingredient`).on('click',function(){
        if(confirm("Are you sure?")) {
            var i = $(this).get(0).id.split('-')[2]
            $(`#ingredient-${i}`).hide();
                $(`#ingredient-${i}`).children().find('input').attr("disabled", true);
        }
    });

    $('#preview-recipe').click(function(){
        $('#editor-form').attr("target", "_blank")
    });

    $('#delete-recipe').click(function(){
        $('#editor-form').attr("target", "")
    });

    $('#cancel-changes').click(function(){
        $('#editor-form').attr("target", "")
    });

    
});