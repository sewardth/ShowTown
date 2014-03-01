/**
 * @file Functions to handle the trending page content
 */

function init_page(){
  $('li.venues').addClass('selected');
  //
  $('#selected_venue_type').text('All');
  $('#venue_types').empty();
  $('#venue_types')
    .append($(document.createElement('li'))
      .append($(document.createElement('a'))
        .attr({href:'javascript:void(0)'})
        .bind('click',{}, function(e) {
          load_page_content('all', null)
        })
        .text('All')
      )
    );
  for(key in venue_types){
    $('#venue_types')
      .append($(document.createElement('li'))
        .append($(document.createElement('a'))
          .attr({href:'javascript:void(0)'})
          .bind('click',{key: key}, function(e) {
            load_page_content(e.data.key, null, null)
          })
          .text(venue_types[key])
        )
      );
  }
  $('#gig_offers').empty();
  for(text in gig_offers){
    $('#gig_offers')
      .append($(document.createElement('li'))
        .append($(document.createElement('a'))
          .attr({href:'javascript:void(0)'})
          .bind('click',{key: gig_offers[text]}, function(e) {
            load_page_content(null, null, e.data.key)
          })
          .text(text)
        )
      );
  }
  load_page_content(null, states[$('#selected_state').text()], gig_offers[$('#selected_gig_offer').text()])
}
   
function load_page_content(venue_type, state_code, gig_offer){
console.log('Load venue_type=' + venue_type + ' - state=' + state_code + ' - gig_offer=' + gig_offer)   
  $.ajax({
    type: "POST",
    url: '/venues',
    dataType: 'json',
    data: {venue_type:venue_type, state_code:state_code, gig_offer:gig_offer}})
    .done(function(data, textStatus, xhr){
      var entries = data.venue_data;
      for(var i = 0, len = entries.length; i < len; i++){
        $('#venue_data')
          .append($(document.createElement('tr'))
            .append($(document.createElement('td'))
              .append($(document.createElement('img'))
                .attr({src:entries[i].image_src})
              )
            )
            .append($(document.createElement('td'))
              .append($(document.createElement('h3'))
                .append($(document.createElement('a'))
                  .attr({href:'/venue?id=' + entries[i].venue_id})
                  .text(entries[i].venue_name)
                )
              )
            )
            .append($(document.createElement('td'))
              .append($(document.createElement('a'))
                .attr({href:'#'})
                .text(entries[i].venue_city)
              )
              .append($(document.createElement('span'))
                .text(', ' + entries[i].venue_state)
              )
            )
            .append($(document.createElement('td'))
              .append($(document.createElement('a'))
                .attr({href:'#'})
                .text(entries[i].venue_type)
              )
            )
            .append($(document.createElement('td'))
              .append($(document.createElement('a'))
                .attr({href:'#',  'class':"btn btn-primary signup"})
                .text('Available Gigs')
              )
            )
          );
          
      }// for
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}