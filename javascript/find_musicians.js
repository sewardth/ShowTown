/**
 * @file Functions to handle the trending page content
 */

function init_page(){
  $('li.musicians').addClass('selected');
  
  if(selected_genre != '' || selected_state != ''){
    do_search();
  }
}

function do_search(){
  $.ajax({
    type: "POST",
    url: '/find_musicians',
    dataType: 'json',
    data: {
      genre:$('#genre').val(), 
      state:$('#state-select').val(),
      city:$('#city-select').val(),
      keywords:$('#keywords').val()
    }})
    .done(function(data, textStatus, xhr){
      var entries = data.musicians;
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
                  .html('<i class="fa fa-thumbs-o-up"></i> ' + entries[i].musician_stats.likes + ' Likes and <i class="fa fa-users left_spaced"></i> ' + entries[i].musician_stats.followers + ' Followers')
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
    $.get("/load-content/parameters/city?state="+state,function(data,status){
      $('#city-select').html('');
      for (x in data.cities)
      {

        $('#city-select').append($('<option/>').html(data.cities[x]));
      }

    });
  });
});