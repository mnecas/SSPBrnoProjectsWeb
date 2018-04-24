var elem = document.querySelector('.sidenav');
var instance = M.Sidenav.init(elem, options);

$(document).ready(function(){
  $('.sidenav').sidenav();
});

$(document).ready(function () {
    $('input#input_text, textarea#textarea2').characterCounter();
});

$(document).ready(function () {
    $('.slider').slider({full_width: true});
});