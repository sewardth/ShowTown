/**
 * @file Functions to handle the home page content
 */

function init_page(){
  $('li.musicians').addClass('selected');
  //
  var selected_genre_code = 'alt';
  $('#selected_genre').text(genres[selected_genre_code]);
  $('#genres_list').empty();
  for(key in genres){
    $('#genres_list')
      .append($(document.createElement('li'))
        .append($(document.createElement('a'))
          .attr({href:'javascript:void(0)'})
          .bind('click',{key: key}, function(e) {
            load_page_content(e.data.key, null)
          })
          .text(genres[key])
        )
      );
  }
  $('#genres_list').append($(document.createElement('li')).attr({class:'divider'}))
  $('#genres_list')
    .append($(document.createElement('li'))
      .append($(document.createElement('a'))
        .attr({href:'javascript:void(0)'})
        .bind('click',{}, function(e) {
          load_page_content('random', null)
        })
        .text('Random')
      )
    );
  load_page_content(selected_genre_code, states[$('#selected_state').text()])
}


function load_page_content(genre_code, state_code){
console.log('Load genre=' + genre_code + ' - state=' + state_code)   
  $.ajax({
    type: "POST",
    url: '/',
    dataType: 'json',
    data: {genre_code:genre_code, state_code:state_code}})
    .done(function(data, textStatus, xhr){
      // Left
      $('#left_iframe').attr('src', data.lvideo.url);
      $('#left_musician_name').text(data.lvideo.musician_name);
      $('#left_song_name').text(data.lvideo.song_name);
      // Right
      $('#right_iframe').attr('src', data.rvideo.url);
      $('#right_musician_name').text(data.rvideo.musician_name);
      $('#right_song_name').text(data.rvideo.song_name);
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}