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
  var login_html = '<div id="login">' +
                    '<fieldset><legend>Login to ShowTown</legend>' +
                      '<p id="login_error"></p>' +
  					          '<p class="fl"><label>E-mail</label> <input type="text" name="login_email"></p>' +
  					          '<p class="fl"><label>Password</label> <input type="password" name="login_password"></p>' +
  					          '<p><input class="btn btn-primary" value="Login"type="button" onclick="do_ajax_login()"/> ' +
  					          '<a style="color:blue;" href="/account">I forgot my password</a></p>' +
  				          '</fieldset></div>';
	$('#login_popup_dialog')
	  .append(login_html)  
	  .parent().append('<div class="dialog_close" onclick="global.login_popup_dialog.dialog(\'close\')" title="Close"></div>') 				
		
	global.login_popup_dialog.dialog('open');
	// Reset the width so it doesn't go over.
	$('#login_popup_dialog').attr("style","width:360px;");
}

function do_ajax_login(){
  $('#login_error').text('');
  $.ajax({
    type: "POST",
    url: '/login_handler',
    dataType: 'json',
    data: {url_path:window.location.pathname, email:$("[name='login_email']").val(), password:$("[name='login_password']").val()}})
    .done(function(data, textStatus, xhr){
      if(data.error){
        $('#login_error').text(data.error);
      }else{
        location.reload(true);
      }
    })
    .fail(function(xhr){ 
console.log(xhr)
    });
  
}