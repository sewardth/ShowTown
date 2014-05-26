/**
 * @file Functions to handle the trending page content
 */

function init_page(){
  $('li.trending').addClass('selected');
  // ========================
  // Genres
  $('#selected_genre').text('All');
  $('#genres_list').empty();
  $('#genres_list')
    .append($(document.createElement('li'))
      .append($(document.createElement('a'))
        .attr({href:'javascript:void(0)'})
        .bind('click',{}, function(e) {
          $('#selected_genre').text('All');
          load_page_content('All', states[$('#selected_state').text()])
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
            $('#selected_genre').text(genres[e.data.key]);
            load_page_content(e.data.key, states[$('#selected_state').text()])
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
          $('#selected_genre').text('Random');
          load_page_content('Random', states[$('#selected_state').text()])
        })
        .text('Random')
      )
    );
  // ========================
  // States 
  $('#selected_state').text(Object.keys(states)[0]); 
  $('#states_list').empty();
  for(key in states){
    $('#states_list')
      .append($(document.createElement('li'))
        .append($(document.createElement('a'))
          .attr({href:'javascript:void(0)'})
          .bind('click',{key: states[key]}, function(e) {
            $('#selected_state').text(states[e.data.key]);
            load_page_content($('#selected_genre').text(), e.data.key);
          })
          .text(key)
        )
      );
  }
  load_page_content(null, states[$('#selected_state').text()])
}
   
function load_page_content(genre_code, state_code){
  $.ajax({
    type: "POST",
    url: '/trending',
    dataType: 'json',
    data: {genre_code:genre_code, state_code:state_code}})
    .done(function(data, textStatus, xhr){
      var entries = data.trending_data;
      for(var i = 0, len = entries.length; i < len; i++){
        $('#trending_data')
          .append($(document.createElement('div'))
            .attr({"class":"row prev-vid-row prev-vid"})
            .append($(document.createElement('div'))
              .attr({"class":"col-lg-1"})
              .append($(document.createElement('h1'))
                .text('#' + (i + 1))
              )
            )
            .append($(document.createElement('div'))
              .attr({"class":"col-lg-7"})
              .append($(document.createElement('a'))
                .attr({href:"/musician?id=" + encodeURIComponent(entries[i].mus_key)})
                .append($(document.createElement('img'))
                  .attr({'class':"pull-left artist_image", src:'/imgs?id=' + encodeURIComponent(entries[i].mus_key) + '&width=100&height=100'})
                )
              )
              .append($(document.createElement('h4'))
                .append($(document.createElement('a'))
                  .attr({href:"/musician?id=" + encodeURIComponent(entries[i].mus_key)})
                  .text(entries[i].band_name)
                )
                .append($(document.createElement('small'))
                  .attr({'class':'left_spaced'})
                  .text(entries[i].likes_count + ' Likes and ' + entries[i].followers_count + ' Followers')
                )
              )
              .append($(document.createElement('p'))
                .append($(document.createElement('strong'))
                  .text('Genre:')
                )
                .append($(document.createElement('a'))
                  .attr({href:"#"})
                  .text(entries[i].band_genre)
                )
                .append($(document.createElement('br')))
                .append($(document.createElement('span'))
                  .text('Located in ' + entries[i].address[0].city + ', ')
                )
                .append($(document.createElement('a'))
                  .attr({href:"#"})
                  .text(entries[i].musician_state)
                )
              )
            )
            .append($(document.createElement('div'))
              .attr({"class":"col-lg-4"})
              .append($(document.createElement('h1'))
                .attr({'class':"text-center"})
                .text(entries[i].like_percent + '%')
              )
              .append($(document.createElement('p'))
                .attr({'class':"text-center liked"})
                .text('Liked ' + entries[i].like_percent + '% of the time')
              )
            )
          );
      }// for
            
            
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}