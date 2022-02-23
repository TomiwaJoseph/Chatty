

$(document).ready(function(){

    let triggered = false;
    let the_strong = "";
    let alert_type = "";

    $('.contacts li').on('click', function (){
        $('.contacts .active').removeClass('active');
        $(this).addClass('active');
        $.ajax({
            url: '/show_chat_messages/',
            dataType: 'json',
            success: function(response){
                $('#action_container').html(response.conversation);
            }
        });
    })

    $('.chat_search_form').submit(function (e) {
        e.preventDefault();
        console.log('form submitted');
        $.ajax({
            url: '/',
            type: 'POST',
            data: $('.chat_search_form').serialize(),
            success: function(response) {
                console.log('success response')
                // $('#product_container').html(res.filtered_products);
            }
        })
    })

    $('.user_action_menu li').on('click', function () {
        var button = $(this).data('name');
        if (button == 'User profile'){
            $.ajax({
                url: '/show_user_profile/',
                dataType: 'json',
                success: function(response){
                    $('#action_container').html(response.profile);
                    if (triggered) {
                        $('.msg_container').css('display', 'block');
                        $('.msg_container a').html('&times;')
                        $('.msg_container strong').html(the_strong)
                        $('.msg_container #the_alert').addClass('alert-'+alert_type)
                        triggered = false;

                    } else {
                        $('.msg_container').css('display', 'none');
                        $('.profile').css('padding-top', '100px');
                        the_a = "";
                        the_strong = "";
                    }
                }
            });
        } else if (button == 'Edit profile') {
            $.ajax({
                url: '/show_user_edit_profile/',
                dataType: 'json',
                success: function(response){
                    $('#action_container').html(response.forms);
                }
            });
        } else if (button == 'Change password') {
            $.ajax({
                url: '/show_user_edit_password/',
                dataType: 'json',
                success: function(response){
                    $('#action_container').html(response.form);
                }
            });
        }
    })

    $('body').on('click', '#profile_save_btn', function(event) {
        event.preventDefault();
        csrftoken = $('[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: '/update_user_profile/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: $('#change_profile_details').serialize(),
            success: function(response){
                $('#view_profile').trigger('click');
                triggered = true;
                the_strong = "Profile updated successfully!";
                alert_type = 'success'
            },
        });
    })

    $('body').on('click', '#password_save_btn', function(event) {
        event.preventDefault();
        csrftoken = $('[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: '/update_user_password/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: $('#change_password_details').serialize(),
            success: function(response){
                console.log(response.status);
                $('#view_profile').trigger('click');
                triggered = true;
                if (response.status == 'success'){
                    the_strong = "Password updated successfully! Enjoy.";
                    alert_type = 'success'
                } else if (response.status == 'failure'){
                    the_strong = "Password update fail! Wrong old password.";
                    alert_type = 'danger'
                }
            },
        });
    })


})