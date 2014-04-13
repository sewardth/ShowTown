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
                .attr({src:'/imgs?id='+entries[i].venue_key+'&width=210&height=119'})
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
              .text(entries[i].address[0].city + ', ' + entries[i].address[0].state)
            )
            .append($(document.createElement('td'))
              .text(entries[i].venue_type)
            )
            .append(user_type == 'musician' ? $(document.createElement('td'))
              .append($(document.createElement('a'))
                .attr({href:'javascript:void(0)',  'class':"btn btn-primary signup"})
                .bind('click',{venue_id:entries[i].venue_key}, function(e){
                  $.ajax({
                    type: "POST",
                    url: '/available_gig?id=' + encodeURIComponent(e.data.venue_id),
                    dataType: 'json',
                    data: {}})
                    .done(function(data, textStatus, xhr){
                      show_available_gigs_popup(e.data.venue_id, data);
                    })
                    .fail(function(xhr){ 
console.log(xhr)
                    });
                })
                .text('Available Gigs')
              ) : null
            )
          );
          
      }// for
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}

function show_available_gigs_popup(venue_id, data){
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
	}
	var available_gigs_html = '<div class="microcopy"><div><h2>Gigs at ' + data.venue.venue_name + ' <small>' + 
	  data.venue.venue_type + '</small></h2></div><div>' + data.venue.address[0].address_1 + ', ' + data.venue.address[0].city +
	  ', ' + data.venue.address[0].state + ' ' + data.venue.address[0].zip + '</div><div><b>Ph: </b>' + 
	  data.venue.phone + ' | <b>Web: </b><a href="' + data.venue.venue_url + '" target="_blank">' + data.venue.venue_url + 
	  '</a></div></div>';
	if(data.gigs.length == 0){
	  available_gigs_html += '<div>None</div>';
	}else{
	  available_gigs_html += '<table class="table microcopy gigs"><thead><tr><th>Gig Name</th><th>Date / Time</th><th>Details</th><th>Compensation</th><th>&nbsp;</th></tr></thead><tbody>';
	  for(gig_idx in data.gigs){
  	  available_gigs_html += '<tr><td>' + data.gigs[gig_idx].gig_name + '</td><td><b>' + data.gigs[gig_idx].event_date + 
  	    '</b><br/>' + data.gigs[gig_idx].start_time + ' - ' + data.gigs[gig_idx].end_time +
  	    '</td><td><ul><li>' + data.gigs[gig_idx].locality + ' Musicians Only</li></ul><p>' + data.gigs[gig_idx].description + 
  	    '</p></td><td>$' + data.gigs[gig_idx].compensation + '</td><td>' +
  	    '<a class="btn btn-primary" href="javascript:void(0)" onclick="show_available_gigs_apply(\'' + data.gigs[gig_idx].gig_key + '\')">Apply</a></td></tr>';
  	}
  	available_gigs_html += '</tbody></table>';
	}
	$('#generic_popup_dialog').empty();
	$('#generic_popup_dialog')
	  .append(available_gigs_html)  
	  .parent().append('<div class="dialog_close" onclick="global.available_gigs_popup_dialog.dialog(\'close\')" title="Close"></div>');				
		
	global.available_gigs_popup_dialog.dialog('open');
	// Reset the width so it doesn't go over.
	$('#generic_popup_dialog').attr("style","width:900px;");
}

function show_available_gigs_apply(gig_key){
  global.available_gigs_popup_dialog.dialog('close');
  $.ajax({
    type: "POST",
    url: '/apply_window_gig',
    dataType: 'json',
    data: {id:gig_key}})
    .done(function(data, textStatus, xhr){
      show_apply_gig_popup(data);
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}

function show_apply_gig_popup(data){
  if(global.apply_gig_popup_dialog == undefined){
		global.apply_gig_popup_dialog = $('#generic_popup_dialog2').dialog({ 
			autoOpen: false,
			modal: true, 
			width: 'auto',
			height: 'auto',
			position: Array(250,100),
			resizable: false,
			overlay: { 
				opacity: 0.8, 
				background: "black" 
			},
		});
	}
	var video_options = '';
	for(var i = 0, len = data.videos.length; i < len; i++){
    video_options += '<option value="' + data.videos[i].video_key + '">' + data.videos[i].video_title + '</option>';
  }
	var apply_gig_html = '<div class="microcopy"><div><h2>Apply to Play at ' + data.venue.venue_name + ' <small>$' + 
	  data.gig.compensation + '</small></h2></div><div><b>' + data.gig.gig_name + '</b></div><div><b>' + 
	  data.gig.event_date + '</b> ' + data.gig.start_time + ' - ' + data.gig.end_time + '</div>' +
	  '<div><b>Details</b></div>' +
	  '<div><b>Description</b></div><div>' + data.gig.description + '</div>' +
	  '<div class="notice">' +
	  '<h4>You meet the criteria for this gig</h4>' +
    '<p>Please select a video to send to this venue as an application</p>' +
    '<p><select id="selected_video">' + video_options + '</select></p>' + 
    '<p"><a class="btn btn-primary" href="javascript:void(0)" onclick="apply_to_gig(\'' + data.gig.gig_key + '\')">Apply</a></p>' +
	  '</div>';
	
	$('#generic_popup_dialog2').empty();
	$('#generic_popup_dialog2')
	  .append(apply_gig_html)  
	  .parent().append('<div class="dialog_close" onclick="global.apply_gig_popup_dialog.dialog(\'close\')" title="Close"></div>');
	  
	global.apply_gig_popup_dialog.dialog('open');
	// Reset the width so it doesn't go over.
	$('#generic_popup_dialog2').attr("style","width:650px;");
}

function apply_to_gig(gig_key){
  var selected_video = $('#selected_video').val();
  global.apply_gig_popup_dialog.dialog('close');
  $.ajax({
    type: "POST",
    url: '/apply_to_gig',
    dataType: 'json',
    data: {id:gig_key, vid_key:selected_video}})
    .done(function(data, textStatus, xhr){

    })
    .fail(function(xhr){ 
console.log(xhr)
    });
}