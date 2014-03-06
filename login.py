import webapp2, sys, uuid
sys.path.insert(0,'libs')
import models, views
from login.password import Passwords as pwd
from login.session import Session as ses
from helpers import messages

class login(views.Template):
  def post(self):
	password = self.request.get('password')
	email = self.request.get('email')
	
	user = models.account.Account.query_by_email(email)
	if user == None:
		messages.Message('User not found.  Please verify the email: ' + email)
	else:
		check = pwd.compare_hash(password, stored_password.password)
	
	
	if check == True:   #add and user.verified == True after testing
		user.session_token = uuid.uuid4().put()
		
		#builds cookies
		user_cookie = ses.create_cookie('user_id', user.key)
		session_cookie = ses.create_cookie('session_id', user.session_token)
		self.response.headers.add_header('Set-Cookie', user_cookie + '; Path=/')
		self.response.headers.add_header('Set-Cookie', session_cookie + '; Path=/')
		
	else:
		messages.Message('Password does not match the one stored for ' + user.email)
		
		


app = webapp2.WSGIApplication([
    ('/login_handler', login)

], debug=True)