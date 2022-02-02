$(document).ready(function () {

    $('#search').click(function (e) {
        e.preventDefault();
        $('.navbar form').fadeToggle();
        document.getElementById("search_text").focus();
    });

    $('.search_form')

});