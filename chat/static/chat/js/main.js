$(document).ready(function () {

    $(function () {
        $('input').blur();
    })

    $('#user_action_menu_btn').on('click', function () {
        $('.user_action_menu').fadeToggle();
    })

    $('#action_menu_btn').on('click', function () {
        $('.action_menu').fadeToggle();
    })
    
    $('.message_tins .fa-search').on('click', function(e) {
        e.stopPropagation();
        $('.chat_search_form').fadeToggle();
        document.getElementById("search_text").focus();
    });

    $('.contacts_card .fa-plus').on('click', function(e) {
        $('.contact_add_form').fadeToggle();
        document.getElementById("add_new_cont").focus();
        if ($('.contact_search').is(':visible')) {
            $('.contact_search').fadeOut();
        } else {
            $('.contact_search').fadeIn();
        }
    });

    $(document).click(function (e) {
        if(!$(e.target).closest('.chat_search_form').length){
            $('.chat_search_form').fadeOut();
        }
        if(!$(e.target).closest('#user_action_menu_btn').length){
            $('.user_action_menu').fadeOut();
        }
        if(!$(e.target).closest('#action_menu_btn').length){
            $('.action_menu').fadeOut();
        }
        if(!$(e.target).closest('#add_cont').length){
            $('.contact_add_form').fadeOut();
            $('.contact_search').fadeIn();
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