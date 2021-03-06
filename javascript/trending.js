/**
 * @file Functions to handle the trending page content
 */

function init_page(){
  $('li.trending').addClass('selected');
  // ========================
  // Genres
  $('#selected_genre span').text('All');
  $('#genres_list').empty();
  $('#genres_list')
    .append($(document.createElement('li'))
      .append($(document.createElement('a'))
        .attr({href:'javascript:void(0)'})
        .bind('click',{}, function(e) {
          $('#selected_genre span').text('All');
          load_page_content('All', states[$('#selected_state span').text()])
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
            $('#selected_genre span').text(genres[e.data.key]);
            load_page_content(e.data.key, states[$('#selected_state span').text()])
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
          $('#selected_genre span').text('Random');
          load_page_content('Random', states[$('#selected_state span').text()])
        })
        .text('Random')
      )
    );
  // ========================
  // States 
  $('#selected_state span').text(selected_state == '' ? Object.keys(states)[0] : selected_state); 
  $('#states_list').empty();
  states['All'] = 'All';
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
 
function variableType(stat)
{
    if (stat === undefined)
    {
        return 0;
    }
    else
    {
        return stat;
    }
}

 
function load_page_content(genre_code, state_code){
  $.ajax({
    type: "POST",
    url: '/trending',
    dataType: 'json',
    data: {genre_code:genre_code, state_code:state_code}})
    .done(function(data, textStatus, xhr){
      $('#trending_data').empty();
      if (data.error){
        $('#trending_data').html(data.error);
      }else{
        var entries = data.trending_data;
        for(var i = 0, len = entries.length; i < len; i++){
          // Create the span for multiple genres.
          var gen_span = $(document.createElement('span'));
          for(var g = 0, len2 = entries[i].band_genre.length; g < len2; g++){
            $(gen_span)
              .append($(document.createElement('a'))
                .attr({href:"/find_musicians?g=" + encodeURIComponent(entries[i].band_genre[g])})
                .text((g > 0 ? ', ' : '') + entries[i].band_genre[g])
              )
          }
          var likes = variableType(entries[i].musician_stats.likes);
          var wins = variableType(entries[i].musician_stats.head_to_head_wins);
          var followers = variableType(entries[i].musician_stats.followers);
          var total_matchups = variableType(entries[i].musician_stats.total_matchups);
          if (wins != 0){
            var win_percent = Math.round((wins / total_matchups)*100);
          }else{
            var win_percent = 0;
          }
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
                    .attr({'class':"pull-left artist_image", src:'/imgs?id=' + encodeURIComponent(entries[i].key) + '&width=100&height=100'})
                  )
                )
                .append($(document.createElement('h4'))
                  .append($(document.createElement('a'))
                    .attr({href:"/musician?id=" + encodeURIComponent(entries[i].key)})
                    .text(entries[i].band_name)
                  )
                  .append($(document.createElement('span'))
                    .attr({'class':'left_spaced microcopy informational middle'})
                    .html('<i class="fa fa-thumbs-o-up"></i> ' + (likes+wins) + ' Likes and <i class="fa fa-users left_spaced"></i> ' + followers + ' Followers')
                  )
                )
                .append($(document.createElement('p'))
                  .append($(document.createElement('strong'))
                    .text('Genre: ')
                  )
                  .append(gen_span)
                  .append($(document.createElement('br')))
                  .append($(document.createElement('span'))
                    .text('Located in ' + entries[i].address[0].city + ', ')
                  )
                  .append($(document.createElement('a'))
                    .attr({href:"/find_musicians?s=" + encodeURIComponent(entries[i].musician_state)})
                    .text(entries[i].musician_state)
                  )
                )
              )
              .append($(document.createElement('div'))
                .attr({"class":"col-lg-4"})
                .append($(document.createElement('h1'))
                  .attr({'class':"text-center"})
                  .text(win_percent + '%')
                )
                .append($(document.createElement('p'))
                  .attr({'class':"text-center liked"})
                  .text('Liked ' + win_percent + '% of the time')
                )
              )
            );
        }// for
      }// if (data.error)    
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}