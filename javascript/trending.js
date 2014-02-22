/**
 * @file Functions to handle the trending page content
 */

function init_page(){
  $('li.trending').addClass('selected');
  //
  $('#selected_genre').text('All');
  $('#genres_list').empty();
  $('#genres_list')
    .append($(document.createElement('li'))
      .append($(document.createElement('a'))
        .attr({href:'javascript:void(0)'})
        .bind('click',{}, function(e) {
          load_page_content('all', null)
        })
        .text('All')
      )
    );
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
  load_page_content(null, states[$('#selected_state').text()])
}
   
function load_page_content(genre_code, state_code){
console.log('Load genre=' + genre_code + ' - state=' + state_code)   
  $.ajax({
    type: "POST",
    url: '/get_trending_page_data',
    dataType: 'html',
    data: {genre_code:genre_code, state_code:state_code}})
    .done(function(data, textStatus, xhr){
console.log(data)      
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}