$(document).ready(function(){
    $('.link_up').click(function(){
        console.log('.link_up clicked right!');
        var linkid;
        linkid = $(this).attr("linkid");
        $.get('/news/up_link/', {'linkid': linkid}, function(data){
                   console.log(data);
                   if(data=='/news/login/')
                   {
                       console.log('jump');
                       window.location.href=data;
                   }
                   else {
                       //$('#score').html(data);
                       //score = '#score' + linkid;
                       //up = '#up' + linkid;
                       //console.log(score);
                       $(score).html(data);
                       $(up).hide();
                   }
        });
    });

});
