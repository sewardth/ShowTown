$( document ).ready(function() {
  set_top_menu();
});

function set_top_menu(){
  var a = $('<a>', { href:window.location } )[0];
  console.log(a.hostname);
  console.log(a.pathname);
  switch(a.pathname){
    case '/':
      $('li.musicians').addClass('selected');
      break;
    case '/trending':
      $('li.trending').addClass('selected');
      break;
    case '/venues':
      $('li.venues').addClass('selected');
      break;
  }
}