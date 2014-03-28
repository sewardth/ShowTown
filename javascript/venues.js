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
                .attr({src:'/imgs?id='+entires[i].venue_key+'&width=210&height=119')
              )	
            )
            .append($(document.createElement('td'))
              .append($(document.createElement('h3'))
                .append($(document.createElement('a'))
                  .attr({href:'/venue?id=' + entries[i].venue_key})
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
                .attr({href:'javascript:void(0)',  'class':"btn btn-primary signup"})
                .bind('click',{venue_id:entries[i].venue_key}, function(e){
                  show_available_gigs_popup(e.data.venue_id)
                })
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

function show_available_gigs_popup(venue_id){
  if(global.available_gigs_popup_dialog == undefined){
		global.available_gigs_popup_dialog = $('#generic_popup_dialog').dialog({ 
			autoOpen: false,
			modal: true, 
			width: 'auto',
			height: 'auto',
			position: Array(150,100),
			resizable: false,
			overlay: { 
				opacity: 0.8, 
				background: "black" 
			},
		});
		global.available_gigs_popup_dialog.dialog( "option", "title", "Add a video" );
	}
	$('#generic_popup_dialog').empty();
  var available_gigs_html = '<div id="available_gigs"><h2>Avaliable gigs for </h2><br/>venue_id=' + venue_id + '</div>';
	$('#generic_popup_dialog')
	  .append(available_gigs_html)  
	  .parent().append('<div class="dialog_close" onclick="global.available_gigs_popup_dialog.dialog(\'close\')" title="Close"></div>') 				
		
	global.available_gigs_popup_dialog.dialog('open');
	// Reset the width so it doesn't go over.
	$('#generic_popup_dialog').attr("style","width:900px;");
}