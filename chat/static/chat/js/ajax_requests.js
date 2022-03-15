

$(document).ready(function(){

    $('.message_tins #view_contact_profile').on('click', function() {
        let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
        other_user_id = $.trim(other_user_id)
        $.ajax({
            url: '/show_contact_profile/',
            data: {
                other_user_id: other_user_id
            },
            dataType: 'json',
            success: function(response){
                $('#contactProfileModal .modal-body h1').html(response.user_profile)
                $('#contactProfileModal .modal-body .email').html(response.user_email)
                $('#contactProfileModal .modal-body img').attr('src', response.user_picture)
                $('#contactProfileModal .modal-body .stat').html(response.user_status)
                $('#contactProfileModal .modal-body .desc').html(response.user_description)
                $('#contactProfileModal').modal('show');
            }
        });
    })

    $('.user_action_menu li').on('click', function () {
        var button = $(this).data('name');
        if (button == 'User profile'){
            $.ajax({
                url: '/show_user_profile/',
                dataType: 'json',
                success: function(response){
                    $('#userProfileModal .modal-body h1').html(response.user_profile)
                    $('#userProfileModal .modal-body .email').html(response.user_email)
                    $('#userProfileModal .modal-body img').attr('src', response.user_picture)
                    $('#userProfileModal .modal-body .stat').html(response.user_status)
                    $('#userProfileModal .modal-body .desc').html(response.user_description)
                    $('#userProfileModal').modal('show');
                }
            });
        } else if (button == 'Edit profile') {
            $('#editProfileModal').modal("show");
        } else if (button == 'Change password') {
            $('#editPasswordModal').modal("show");
        }
    })

    $('#add_contact_form').submit(function(event) {
        event.preventDefault();
        csrftoken = $('[name=csrfmiddlewaretoken]').val();
        $('#addContactModal').modal('hide')
        $.ajax({
            url: '/add_contact/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: $('#add_contact_form').serialize(),
            success: function(response) {
                if (response.status == 'success') {
                    $('#statusModal .modal-body h4').html('Success!')
                    $('#statusModal .icon-box i').html('&#10003;')
                    $('#statusModal .modal-body span').html('Refresh Page')
                    $('#statusModal .modal-header').css('background', '#28a745')
                    $('#statusModal .modal-body p').html('Contact added successfully. Please refresh your page for this change to take effect.')
                    $('#statusModal').modal('show');
                } else if (response.status == 'same user') {
                    $('#statusModal .modal-body h4').html('Info!')
                    $('#statusModal .icon-box i').html('&#33;')
                    $('#statusModal .modal-body span').html('Continue')
                    $('#statusModal .modal-header').css('background', '#17a2b8')
                    $('#statusModal .modal-body p').html("You can't chat with yourself! If you want to do it, do it in the confort of your home...alone.")
                    $('#statusModal').modal('show');
                } else if (response.status == 'blocked thread') {
                    $('#statusModal .modal-body h4').html('Info!')
                    $('#statusModal .icon-box i').html('&#33;')
                    $('#statusModal .modal-body span').html('Go Back')
                    $('#statusModal .modal-header').css('background', '#17a2b8')
                    $('#statusModal .modal-body p').html('For some reason you cannot add this contact. Contact admin for more information about this.')
                    $('#statusModal').modal('show');
                } else if (response.status == 'existing thread') {
                    $('#statusModal .modal-body h4').html('Info!')
                    $('#statusModal .icon-box i').html('&#33;')
                    $('#statusModal .modal-body span').html('Continue')
                    $('#statusModal .modal-header').css('background', '#17a2b8')
                    $('#statusModal .modal-body p').html('You already have this contact in your contacts list.')
                    $('#statusModal').modal('show');
                } else if (response.status == 'unknown contact') {
                    $('#statusModal .modal-body h4').html('Error!')
                    $('#statusModal .icon-box i').html('&#10761;')
                    $('#statusModal .modal-body span').html('Go Back')
                    $('#statusModal .modal-header').css('background', '#dc3545')
                    $('#statusModal .modal-body p').html('Unknown user. This user is not registered with us.')
                    $('#statusModal').modal('show');
                }
            }
        })
    })

    $('#report_user_form').submit(function(event) {
        event.preventDefault();
        var formData = new FormData();
        let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
        other_user_id = $.trim(other_user_id)
        csrftoken = $('[name=csrfmiddlewaretoken]').val();
        formData.append('subject', $('#subject').val());
        formData.append('reason', $('#reason').val());
        formData.append('evidence', $('#evidence')[0].files[0]);
        formData.append('other_user_id', other_user_id);
        formData.append('csrfmiddlewaretoken', csrftoken);
        $('#reportUserModal').modal('hide');
        $('#pleaseWaitModal .modal-header').css('background', '#17a2b8')
        $('#pleaseWaitModal').modal('show');
        $.ajax({
            url: '/report_contact/',
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function(response) {
                $('#pleaseWaitModal').modal('hide');
                $('#statusModal .modal-body h4').html('Success!')
                $('#statusModal .icon-box i').html('&#10003;')
                $('#statusModal .modal-body span').html('Keep Chatting')
                $('#statusModal .modal-header').css('background', '#28a745')
                $('#statusModal .modal-body p').html('Your report about ' + response.the_contact + ' has been taken note of. We will get back to you soon.')
                $('#statusModal').modal('show');
            }
        })
    })

    $('#change_profile_details').submit(function(event) {
        event.preventDefault();
        var form = $('#change_profile_details')[0];
        var form_data = new FormData(form)
        form_data.append('profile_picture', $('#profile_picture')[0].files[0])
        $('#editProfileModal').modal('hide')
        $.ajax({
            url: '/update_user_profile/',
            type: 'POST',
            data: form_data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#statusModal .modal-body h4').html('Success!')
                $('#statusModal .icon-box i').html('&#10003;')
                $('#statusModal .modal-body span').html('Keep Chatting')
                $('#statusModal .modal-header').css('background', '#28a745')
                $('#statusModal .modal-body p').html('Your account has been updated successfully. Kindly refresh this page to see effect take place.')
                $('#statusModal').modal('show');
            }
        })
    })

    $('#change_password_details').submit(function(event) {
        event.preventDefault();
        csrftoken = $('[name=csrfmiddlewaretoken]').val();
        $('#editPasswordModal').modal('hide')
        $.ajax({
            url: '/update_user_password/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: $('#change_password_details').serialize(),
            success: function(response) {
                if (response.status == 'success') {
                    $('#statusModal .modal-body h4').html('Success!')
                    $('#statusModal .icon-box i').html('&#10003;')
                    $('#statusModal .modal-body span').html('Keep Chatting')
                    $('#statusModal .modal-header').css('background', '#28a745')
                    $('#statusModal .modal-body p').html('Your password has been updated successfully.')
                    $('#statusModal').modal('show');
                } else if (response.status == 'failure') {
                    $('#statusModal .modal-body h4').html('Error!')
                    $('#statusModal .icon-box i').html('&#10761;')
                    $('#statusModal .modal-body span').html('Try Again')
                    $('#statusModal .modal-header').css('background', '#dc3545')
                    $('#statusModal .modal-body p').html('Password update fail! Wrong old password.')
                    $('#statusModal').modal('show');
                }
            }
        })
    })

})
