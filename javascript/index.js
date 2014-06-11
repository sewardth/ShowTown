/**
 * @file Functions to handle the home page content
 */

function init_page(){
  $('li.musicians').addClass('selected');
  //
  // ========================
  // Genres
  $('#genres_list').empty();
  for(key in genres){
    $('#genres_list')
      .append($(document.createElement('li'))
        .append($(document.createElement('a'))
          .attr({href:'javascript:void(0)'})
          .bind('click',{key: key}, function(e) {
            $('#selected_genre span').text(genres[e.data.key]);
            load_page_content(e.data.key, states[$('#selected_state span').text()])
          })
          .text(genres[key])
        )
      );
  }
  // ========================
  // States 
  $('#selected_state span').text(Object.keys(states)[0]); 
  $('#states_list').empty();
  for(key in states){
    $('#states_list')
      .append($(document.createElement('li'))
        .append($(document.createElement('a'))
          .attr({href:'javascript:void(0)'})
          .bind('click',{key: key}, function(e) {
            $('#selected_state span').text(e.data.key);
            load_page_content($('#selected_genre span').text(), states[e.data.key]);
          })
          .text(key)
        )
      );
  }
  load_page_content(null, states[$('#selected_state span').text()])
}


function load_page_content(genre_code, state_code){
console.log('Load genre=' + genre_code + ' - state=' + state_code)   
  $.ajax({
    type: "POST",
    url: '/',
    dataType: 'json',
    data: {genre_code:genre_code, state_code:state_code}})
    .done(function(data, textStatus, xhr){
      // Update genre selection
      $('#selected_genre span').text(data.genre_tag);
      // Title
      $('#matchup_title').text(data.genre_tag + ' Matchup');
      // Left

      if (data.response != ''){
        $('#video-matchup').hide();
        $('#draw-div').hide();
        $('#prev-match').hide();
        $('#error').html(data.response);
      }
      else{
        $('#video-matchup').show();
        $('#error').html('');
        $('#left_iframe').attr('src', data.lvideo.url);
  	    $('#left_url').attr('href','/vote?left_vid=' + data.lvideo.key + '&left_mus_id=' +data.lvideo.musician_id + '&left_mus_name=' +data.lvideo.musician_name+ '&right_vid=' +data.rvideo.key+ '&right_mus_id=' +data.rvideo.musician_id + '&right_mus_name=' +data.rvideo.musician_name +'&win=' + data.lvideo.key + '&mus_win=' + data.lvideo.musician_id)
        $('#left_musician_name').text(data.lvideo.musician_name);
        $('#left_song_name').text(data.lvideo.song_name);
        $('#left_image').attr({src:'/imgs?id=' + encodeURIComponent(data.lvideo.musician_id) + '&width=100&height=100'});
        // Right
        $('#right_iframe').attr('src', data.rvideo.url);
  	    $('#right_url').attr('href','/vote?left_vid=' + data.lvideo.key + '&left_mus_id=' +data.lvideo.musician_id + '&left_mus_name=' +data.lvideo.musician_name+ '&right_vid=' +data.rvideo.key+ '&right_mus_id=' +data.rvideo.musician_id + '&right_mus_name=' +data.rvideo.musician_name +'&win=' + data.rvideo.key + '&mus_win=' + data.rvideo.musician_id)
        $('#right_musician_name').text(data.rvideo.musician_name);
        $('#right_song_name').text(data.rvideo.song_name);
        $('#right_image').attr({src:'/imgs?id=' + encodeURIComponent(data.rvideo.musician_id) + '&width=100&height=100'});
  	  // Draw
        $('#draw_url').attr('href','/vote?left_vid=' + data.lvideo.key + '&left_mus_id=' +data.lvideo.musician_id + '&left_mus_name=' +data.lvideo.musician_name+ '&right_vid=' +data.rvideo.key+ '&right_mus_id=' +data.rvideo.musician_id + '&right_mus_name=' +data.rvideo.musician_name +'&win=')
        $('#draw-div').show();
    }})
    .fail(function(xhr){ 
console.log(xhr);
	$('#error').text('No new match-ups at this time.  Please check back later and thank you for voting!');
  $('#video-matchup').hide();
  $('#draw-div').hide();
  $('#selected_genre').text('All');
    });
}