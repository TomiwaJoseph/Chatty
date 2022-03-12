$(document).ready(function () {

    $(function () {
        $('input').blur();
    })

    $('.message_tins #report_contact').on('click', function() {
        $('#reportUserModal').modal("show")
    })

    $('#statusModal .modal-body span').on('click', function() {
        innerText = $(this).html()
        if (innerText == "Refresh Page"){
            location.reload();
        }
    })

    $('.message_tins #search_chat_text').on('click', function() {
        // $('#searchChatModal').modal("show");
        $('#statusModal .modal-body h4').html('Info!')
        $('#statusModal .icon-box i').html('&#33;')
        $('#statusModal .modal-body span').html('Continue Chatting')
        $('#statusModal .modal-header').css('background', '#17a2b8')
        $('#statusModal .modal-body p').html('Simply press Ctrl + F to use the powerful in-built browser finder to find your chat message. This fine utility is not available at this time.')
        $('#statusModal').modal('show');
    })

    $('#add_cont').on('click', function() {
        $('#addContactModal').modal("show")
    })

    $('#nxt_action').on('click', function() {
        error_status = $(this).html()
        if (error_status == "Try Again") {
            $('#editPasswordModal').modal('show');
        }
    })

    $('#user_action_menu_btn').on('click', function () {
        $('.user_action_menu').fadeToggle();
    })

    $('.message_tins #action_menu_btn').on('click', function () {
        $('.action_menu').fadeToggle();
    })

    $(document).click(function (e) {
        if(!$(e.target).closest('#user_action_menu_btn').length){
            $('.user_action_menu').fadeOut();
        }
        if(!$(e.target).closest('#action_menu_btn').length){
            $('.action_menu').fadeOut();
        }
    });

    const picker = new EmojiButton({
        showAnimation: true,
        autoHide: false,
        theme: 'dark',
        rows: 4,
    });

    const trigger = document.querySelector('.emoji_prepend');

    picker.on('emoji', selection => {
        document.querySelector('#input-message').value += selection;
    })

    trigger.addEventListener('click', () => {
        picker.togglePicker(trigger);
    });

});