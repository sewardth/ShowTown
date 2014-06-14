/**
 * @file Functions to handle the trending page content
 */

function init_page(){
  $('li.musicians').addClass('selected');
  
  if(selected_genre != '' || selected_state != ''){
    do_search();
  }
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

function do_search(){
  $.ajax({
    type: "POST",
    url: '/find_musicians',
    dataType: 'json',
    data: {
      genre:$('#genre-select').val(), 
      state:$('#state-select').val(),
      city:$('#city-select').val(),
      keywords:$('#keywords').val()
    }})
    .done(function(data, textStatus, xhr){
      $('#musician_data').empty();
      var entries = data.musicians;
      if (data.error)
      {
        $('#musician_data').text(data.error)
      }
      for(var i = 0, len = entries.length; i < len; i++){
        // Create the span for multiple genres.
        var gen_span = $(document.createElement('span'));
        for(var g = 0, len2 = entries[i].band_genre.length; g < len2; g++){
          var likes = variableType(entries[i].musician_stats.likes);
          var wins = variableType(entries[i].musician_stats.head_to_head_wins);
          var followers = variableType(entries[i].musician_stats.followers);
          $(gen_span)
            .append($(document.createElement('a'))
              .attr({href:"/find_musicians?g=" + encodeURIComponent(entries[i].band_genre[g])})
              .text((g > 0 ? ', ' : '') + entries[i].band_genre[g])
            )
        }
        $('#musician_data')
          .append($(document.createElement('div'))
            .attr({"class":"row prev-vid-row prev-vid"})
            .append($(document.createElement('div'))
              .attr({"class":"col-lg-7"})
              .append($(document.createElement('a'))
                .attr({href:"/musician?id=" + encodeURIComponent(entries[i].key)})
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
          );
      }// for 
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}


//fetch distinct cities based on state selection
$(document).ready(function(){
  $("#state-select").change(function(){
    var state = $('#state-select').val();
    var genre = $('#genre-select').val();
    $.get("/load-content/parameters/city?state="+state+'&genre='+genre,function(data,status){
      $('#city-select').empty();
      for (x in data.cities)
      {

        $('#city-select').append($('<option/>').html(data.cities[x]));
      }

    });
  });


  $("#genre-select").change(function(){
    var genre = $('#genre-select').val();
    $.get("/load-content/parameters/state?genre="+genre,function(data,status){
      $('#state-select').empty();
      for (x in data.states)
      {

        $('#state-select').append($('<option/>').html(data.states[x]));
      }

    });
  });


});