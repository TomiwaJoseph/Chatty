

let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')

const USER_ID = $('#logged-in-user').val()
var logged_user_picture = JSON.parse(JSON.stringify(document.getElementById('logged_user_picture').textContent));
var get_other_user = $('#other_user_picture').html()
var other_user_picture = $.trim(get_other_user)

function findOutTime (time){
    var splittedTime = time.split(" ")
    var theMonth = splittedTime[2]
    var theWeekday = splittedTime[0].slice(0, -1)
    var theDay = splittedTime[1]
    var getTheHours = splittedTime[4].split(':')
    var currentHour = parseInt(getTheHours[0])
    var currentMinute = getTheHours[1]
    var AMPM = (currentHour >= 12) ? "PM" : "AM"
    return theWeekday + " " + theMonth + " " + theDay + ", " + currentHour + ":" + currentMinute + " " + AMPM
}

let loc = window.location
let wsStart = 'ws://'

if(loc.protocol === 'https') {
    wsStart = 'wss://'
}

let endpoint = wsStart + loc.host + loc.pathname
var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    console.log('open', e)
    send_message_form.on('submit', function(e) {
        e.preventDefault();
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()
    
        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': send_to,
            'thread_id': thread_id
        }
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}


function newMessage(message, sent_by_id, thread_id) {
	if ($.trim(message) === '') {
		return false;
    }
    let message_element;
	let chat_id = 'chat_' + thread_id
    if (sent_by_id == USER_ID){
        message_element = `
            <div class="receiver">
                <div class="d-flex replied">
                    <div class="receiver_message_container">
                        ${message}
                    </div>
                    <div class="img_cont_msg">
                        <img src=${logged_user_picture} class="rounded-circle user_img_msg">
                    </div>
                </div>
                <p>${findOutTime(new Date().toUTCString())}</p>
            </div>
        `
    } else {
        message_element = `
            <div class="sender">
                <div class="d-flex received">
                    <div class="img_cont_msg">
                        <img src="${other_user_picture}" class="rounded-circle user_img_msg mb-3">
                    </div>
                    <div class="sender_message_container">
                        ${message}
                    </div>
                </div>
                <p>${findOutTime(new Date().toUTCString())}</p>
            </div>
        `
    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
    message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
	input_message.val(null);
}

$('.contact-li').on('click', function (){
    $('.contacts .active').removeClass('active')
    $(this).addClass('active')

    if (!$('.welcome_greeting').hasClass('d-none')){
        $('.welcome_greeting').addClass('d-none')
    }
    if (!$('.message_tins').hasClass('d-block')){
        $('.message_tins').addClass('d-block')
    }

    // message wrappers
    let chat_id = $(this).attr('chat-id');
    $('.messages-wrapper.is_active').removeClass('is_active');
    $('.messages-wrapper[chat-id="' + chat_id +'"]').addClass('is_active');
    $('.is_active #scroller').scrollTop($('.is_active #scroller')[0].scrollHeight);
})

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}