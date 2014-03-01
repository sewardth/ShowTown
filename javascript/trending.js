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
                .text('#' + entries[i].rank)
              )
            )
            .append($(document.createElement('div'))
              .attr({"class":"col-lg-7"})
              .append($(document.createElement('a'))
                .attr({href:"/musician?id=" + entries[i].musician_id})
                .append($(document.createElement('img'))
                  .attr({'class':"pull-left", src:entries[i].image_src})
                )
              )
              .append($(document.createElement('h4'))
                .append($(document.createElement('a'))
                  .attr({href:"/musician?id=" + entries[i].musician_id})
                  .text(entries[i].musician_name)
                )
                .append($(document.createElement('small'))
                  .text(entries[i].likes_count + ' Likes and ' + entries[i].followers_count + ' Followers')
                )
              )
              .append($(document.createElement('p'))
                .append($(document.createElement('strong'))
                  .text('Genre:')
                )
                .append($(document.createElement('a'))
                  .attr({href:"#"})
                  .text(entries[i].genre)
                )
                .append($(document.createElement('br')))
                .append($(document.createElement('span'))
                  .text('Located in ' + entries[i].musician_city + ', ')
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