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
    url: '/get_venue_page_data',
    dataType: 'html',
    data: {venue_type:venue_type, state_code:state_code, gig_offer:gig_offer}})
    .done(function(data, textStatus, xhr){
console.log(data)      
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}