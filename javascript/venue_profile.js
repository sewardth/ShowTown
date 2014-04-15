/**
 * @file Functions to handle the venue_profile page content
 */

function show_gig_applicants(gig_key){
  $.ajax({
    type: "POST",
    url: '/applicants_profile',
    dataType: 'json',
    data: {id:gig_key}
  })
  .done(function(data, textStatus, xhr){
    global.applicants_data = data.applicants;
    show_gig_applicants_popup(data);
  })
  .fail(function(xhr){ 
console.log(xhr)
  });
}

function show_gig_applicants_popup(data){
  if(global.show_gig_applicants_popup_dialog == undefined){
    global.show_gig_applicants_popup_dialog = $('#generic_popup_dialog').dialog({ 
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
  var gig_applicants_html = '<div class="microcopy"><h2>' + data.applicants[0].gig_name + ' <small>Current Applicants</small></h2><br>' +
 			'<table class="table"><thead><tr>' +
 				'<th>Artist</th><th>Genre</th><th>Total Likes</th><th>Total Followers</th><th>Video</th><th>&nbsp;</th>' +
 				'</tr></thead><tbody>';
  for(idx in data.applicants){
    if(data.applicants[idx].applicant_status && !data.applicants[idx].performing){
      var html_status = '';
      var accept_disabled = '';
      var decline_disabled = '';
    }else if(data.applicants[idx].applicant_status && data.applicants[idx].performing){
      html_status = '<i class="fa fa-check green"></i>';
      var accept_disabled = 'disabled';
      var decline_disabled = '';
    }else{
      var html_status = '<i class="fa fa-times red"></i>';
      var accept_disabled = '';
      var decline_disabled = 'disabled';
    }
    gig_applicants_html += '<tr id="applicant' + idx + '"><td><a href="/musician?id=' + encodeURIComponent(data.applicants[idx].musician_key) + '">' +
      '<img class="pull-left artist_image" src="/imgs?id=' + encodeURIComponent(data.applicants[idx].musician_key) + '&amp;width=100&amp;height=100"></a>' +
      '<h4>' + html_status + '<a href="/musician?id=' + encodeURIComponent(data.applicants[idx].musician_key) + '">' + data.applicants[idx].musician_name + '</a>' +
      '</td><td>' +
      '&nbsp;' +
      '</td><td>' +
      '&nbsp;' +
      '</td><td>' +
      '&nbsp;' +
      '</td><td>' +
      '<a class="btn btn-default signup" href="javascript:void(0)" onclick="show_gig_applicants_watch_video_popup(' + idx + ')">Watch Video</a>' +
      '</td><td>' +
      '<a class="btn btn-primary ' + accept_disabled + ' accept" href="javascript:void(0)" onclick="show_gig_applicants_popup_performers_gig(' + idx + ', \'accept\')">Accept</a> ' +
      '<a class="btn btn-primary ' + decline_disabled + ' decline" href="javascript:void(0)" onclick="show_gig_applicants_popup_performers_gig(' + idx + ', \'decline\')">Decline</a> ' +
      '</td></tr>'
  }
 	gig_applicants_html += '</tbody></table>'			

  $('#generic_popup_dialog').empty();
  $('#generic_popup_dialog')
    .append(gig_applicants_html)  
    .parent().append('<div class="dialog_close" onclick="global.show_gig_applicants_popup_dialog.dialog(\'close\')" title="Close"></div>');        

  global.show_gig_applicants_popup_dialog.dialog('open');
  // Reset the width so it doesn't go over.
  $('#generic_popup_dialog').attr("style","width:900px;");
}

function show_gig_applicants_popup_performers_gig(idx, status){
  if(global.applicants_watch_video_dialog != undefined) global.applicants_watch_video_dialog.dialog('close');
  $.ajax({
    type: "POST",
    url: '/performers_gig',
    dataType: 'json',
    data: {gig_id:global.applicants_data[idx].gig_key, mus_id:global.applicants_data[idx].musician_key, status:status}})
    .done(function(data, textStatus, xhr){
console.log(xhr)
      if(xhr.status == 200){
        // Set checkmark
        var status_html = status == 'accept' ? '<i class="fa fa-check green"></i>' : '<i class="fa fa-times red"></i>';
        $('#applicant' + idx).children('td:first-child').children('h4').prepend(status_html);
        // Disable button
        if(status == 'accept'){
          $('#applicant' + idx).children('td').children('a.accept').addClass('disabled');
        }else{
          $('#applicant' + idx).children('td').children('a.decline').addClass('disabled');
        }
      }
    })
    .fail(function(xhr){ 
console.log(xhr)
      if(xhr.status == 200){
        var status_html = status == 'accept' ? '<i class="fa fa-check green"></i>' : '<i class="fa fa-times red"></i>';
        $('#applicant' + idx).children('td:first-child').children('h4').prepend(status_html);
        if(status == 'accept'){
          $('#applicant' + idx).children('td').children('a.accept').addClass('disabled');
        }else{
          $('#applicant' + idx).children('td').children('a.decline').addClass('disabled');
        }
      }
    });
}

function show_gig_applicants_watch_video_popup(idx){
  global.show_gig_applicants_popup_dialog.dialog('close');
  if(global.applicants_watch_video_dialog == undefined){
    global.applicants_watch_video_dialog = $('#generic_popup_dialog2').dialog({ 
      autoOpen: false,
      modal: true, 
      width: 'auto',
      height: 'auto',
      position: Array(350,100),
      resizable: false,
      overlay: { 
        opacity: 0.8, 
        background: "black" 
      },
    });
  }
  if(global.applicants_data[idx].applicant_status && !global.applicants_data[idx].performing){
    var accept_disabled = '';
    var decline_disabled = '';
  }else if(global.applicants_data[idx].applicant_status && global.applicants_data[idx].performing){
    var accept_disabled = 'disabled';
    var decline_disabled = '';
  }else{
    var accept_disabled = '';
    var decline_disabled = 'disabled';
  }
  var watch_video__html = '<div class="microcopy"><h2 class="text-center">' + global.applicants_data[idx].musician_name + ' <small></small></h2>' +
 			'<div><iframe width="490" height="300" frameborder="0" allowfullscreen="" src="' +
 			global.applicants_data[idx].video_link + '"></iframe></div>' +
 			// <h3 class="text-center">900 Likes. Wins 75% of Match Ups</h3> +
 			'<h3 class="text-center">&nbsp;</h3>' +
 			'<p class="text-center">' +
 			'<a class="btn btn-primary ' + accept_disabled + '" href="javascript:void(0)" onclick="show_gig_applicants_popup_performers_gig(' + idx + ', \'accept\')">Accept</a> ' +
      '<a class="btn btn-primary ' + decline_disabled + '" href="javascript:void(0)" onclick="show_gig_applicants_popup_performers_gig(' + idx + ', \'decline\')">Decline</a> ' +
      '</p></div>';
  
  $('#generic_popup_dialog2').empty();
  $('#generic_popup_dialog2')
    .append(watch_video__html)  
    .parent().append('<div class="dialog_close" onclick="global.applicants_watch_video_dialog.dialog(\'close\')" title="Close"></div>');

  global.applicants_watch_video_dialog.dialog('open');
  // Reset the width so it doesn't go over.
  $('#generic_popup_dialog2').attr("style","width:530px;");
}
