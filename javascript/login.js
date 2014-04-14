/**
 * @file Functions to handle login
 */

function show_login_popup(){
  if(global.login_popup_dialog == undefined){
		global.login_popup_dialog = $('#login_popup_dialog').dialog({ 
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
		global.login_popup_dialog.dialog( "option", "title", "Login" );
	}
	$('#login_popup_dialog').empty();
  var login_html = '<div id="login"><form method="POST" action="/login_handler">' +
                    '<input type="hidden" name="url_path" id="url_path" value="' + window.location.pathname + '" />' +
                    '<fieldset><legend>Login to ShowTown</legend>' +
  					          '<p class="fl"><label>E-mail</label> <input type="text" name="email"></p>' +
  					          '<p class="fl"><label>Password</label> <input type="password" name="password"></p>' +
  					          '<p><input class="btn btn-primary" value="Login"type="submit"/ > <a style="color:blue;" href="/login_handler_reset">I forgot my password</a></p>' +
  				          	  '</fieldset></form></div>';
	$('#login_popup_dialog')
	  .append(login_html)  
	  .parent().append('<div class="dialog_close" onclick="global.login_popup_dialog.dialog(\'close\')" title="Close"></div>') 				
		
	global.login_popup_dialog.dialog('open');
	// Reset the width so it doesn't go over.
	$('#login_popup_dialog').attr("style","width:360px;");
}
