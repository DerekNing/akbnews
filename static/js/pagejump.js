$(document).ready(function(){
    $('#page_jump_button').click(function(){
            var index = $("#page_jump_index").val();
            var url = '/news/?page=' + index;
            window.location.href=url;
    });

    $("#page_jump_index").keydown(function(e){
        if(e.which == 13) {
            var index = $("#page_jump_index").val();
            var url = '/news/?page=' + index;
            console.log(url)
            window.location.href=url;
        }
    });
});
