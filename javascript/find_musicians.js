/**
 * @file Functions to handle the trending page content
 */

function do_search(){
  $.ajax({
    type: "POST",
    url: '/find_musicians',
    dataType: 'json',
    data: {
      genre:$('#genre').val(), 
      popularity:$('#popularity').val(),
      distance:$('#distance').val(),
      keywords:$('#keywords').val()
    }})
    .done(function(data, textStatus, xhr){
      // var entries = data.trending_data;
      // for(var i = 0, len = entries.length; i < len; i++){
      //   $('#trending_data')
      //     .append($(document.createElement('div'))
      //       .attr({"class":"row prev-vid-row prev-vid"})
      //       .append($(document.createElement('div'))
      //         .attr({"class":"col-lg-1"})
      //         .append($(document.createElement('h1'))
      //           .text('#' + (i + 1))
      //         )
      //       )
      //       .append($(document.createElement('div'))
      //         .attr({"class":"col-lg-7"})
      //         .append($(document.createElement('a'))
      //           .attr({href:"/musician?id=" + encodeURIComponent(entries[i].mus_key)})
      //           .append($(document.createElement('img'))
      //             .attr({'class':"pull-left artist_image", src:'/imgs?id=' + encodeURIComponent(entries[i].mus_key) + '&width=100&height=100'})
      //           )
      //         )
      //         .append($(document.createElement('h4'))
      //           .append($(document.createElement('a'))
      //             .attr({href:"/musician?id=" + encodeURIComponent(entries[i].mus_key)})
      //             .text(entries[i].band_name)
      //           )
      //           .append($(document.createElement('small'))
      //             .attr({'class':'left_spaced'})
      //             .text(entries[i].likes_count + ' Likes and ' + entries[i].followers_count + ' Followers')
      //           )
      //         )
      //         .append($(document.createElement('p'))
      //           .append($(document.createElement('strong'))
      //             .text('Genre:')
      //           )
      //           .append($(document.createElement('a'))
      //             .attr({href:"#"})
      //             .text(entries[i].band_genre)
      //           )
      //           .append($(document.createElement('br')))
      //           .append($(document.createElement('span'))
      //             .text('Located in ' + entries[i].address[0].city + ', ')
      //           )
      //           .append($(document.createElement('a'))
      //             .attr({href:"#"})
      //             .text(entries[i].musician_state)
      //           )
      //         )
      //       )
      //       .append($(document.createElement('div'))
      //         .attr({"class":"col-lg-4"})
      //         .append($(document.createElement('h1'))
      //           .attr({'class':"text-center"})
      //           .text(entries[i].like_percent + '%')
      //         )
      //         .append($(document.createElement('p'))
      //           .attr({'class':"text-center liked"})
      //           .text('Liked ' + entries[i].like_percent + '% of the time')
      //         )
      //       )
      //     );
      // }// for
            
            
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}


//fetch distinct cities based on state selection
$(document).ready(function(){
  $("#state-select").change(function(){
    var state = $('#state-select').val();
    $.get("/load-content/parameters/city?state="+state,function(data,status){
      $('#city-select').html('');
      for (x in data.cities)
      {

        $('#city-select').append($('<option/>').html(data.cities[x]));
      }

    });
  });
});