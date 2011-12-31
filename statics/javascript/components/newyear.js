$(function(){
  var date = new Date();
  if(!$.cookie('newyear2012') && date.getYear() == 112 && date.getMonth() == 0 && date.getDate() == 1){
    $img = $('<div>').append($('<img>').attr('src', '/image/2012.png'));
    $('body').append($img);
    $img.lightbox_me();
    $.cookie('newyear2012', true);
  }
});
