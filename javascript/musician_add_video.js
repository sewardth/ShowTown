/**
 * @file Functions to handle add a video
 */

function show_add_video_popup(){
  if(global.add_video_popup_dialog == undefined){
		global.add_video_popup_dialog = $('#generic_popup_dialog').dialog({ 
			autoOpen: false,
			modal: true, 
			width: 'auto',
			height: 'auto',
			position: Array(300,100),
			resizable: false,
			overlay: { 
				opacity: 0.8, 
				background: "black" 
			},
		});
		global.add_video_popup_dialog.dialog( "option", "title", "Add a video" );
	}
	$('#generic_popup_dialog').empty();
  var add_video_html = '<div id="add_video"><form method="POST" action="/video_add">' +
                    '<fieldset><legend>Add a video to your profile</legend>' +
                      '<div class="control-group">' +
                			  '<label for="video_url" class="control-label">Video URL</label>' +
                			  '<div class="controls">' +
                			    '<input type="text" class="input-xlarge" placeholder="http://" name="video_url" id="video_url">' +
                			    '<p class="help-block">Youtube or Vimeo Supported</p>' +
                			  '</div>' +
								'<div class="control-group">'+
				      			  '<label for="video_genre" class="control-label">Video Genre</label>'+
				      			  '<div class="controls">'+
				      			    '<select class="input-xlarge" name="band_genre" id="video_genre">'+
				      			      '<option>Alternative</option>'+
				    		          '<option>Blues</option>'+
				    		          '<option>Classical</option>'+
				    		          '<option>Country</option>'+
				    		          '<option>Dance</option>'+
				    		          '<option>Easy Listening</option>'+
				    		          '<option>Electronic</option>'+
				    		          '<option>Hip-Hop/Rap</option>'+
				    		          '<option>Industrial</option>'+
				    		          '<option>Instrumental</option>'+
				    		          '<option>Jazz</option>'+
				    		          '<option>Pop</option>'+
				    		          '<option>Rock</option>'+
				    		          '<option>Singer/Songwriter</option>'+
				    		          '<option>Vocal</option>'+
				      			    '</select>'+
				      			  '</div>'+
				      			'</div>'+
								'<br>'+
                			'</div>' +
  					          '<p><input class="btn btn-primary" value="Submit"type="submit"/ > ' +
  					          '<input class="btn btn-deemphasize" type="button" onclick="global.add_video_popup_dialog.dialog(\'close\')" value="Cancel" /></p>'
  				          '</fieldset></form></div>';
	$('#generic_popup_dialog')
	  .append(add_video_html)  
	  .parent().append('<div class="dialog_close" onclick="global.add_video_popup_dialog.dialog(\'close\')" title="Close"></div>') 				
		
	global.add_video_popup_dialog.dialog('open');
	// Reset the width so it doesn't go over.
	$('#generic_popup_dialog').attr("style","width:500px;");
}
