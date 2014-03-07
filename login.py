import webapp2, sys, uuid, datetime
sys.path.insert(0,'libs')
import models, views
from sessions.password import Passwords as pwd
from helpers import messages
from helpers.encryption import Encryption as enc

class Login(views.Template):
	def post(self):
		password = self.request.get('password')
		email = self.request.get('email')

		self.user = models.account.Account.query_by_email(email)

		if self.user == None:
			messages.Message.warning('User not found.  Please check the email: ' + email)
		else:
			self.verify_password(password, self.user.password)
			self.set_cookie()


	def verify_password(self, password, pwhash):
		check = pwd.compare_hash(password, pwhash)
		if check == True:   #add and user.verified == True after testing
			self.user.session_token = str(uuid.uuid4())
			self.user.put()
		else:
			messages.Message.warning('Password does not match the one stored for ' + self.user.email)

	def set_cookie(self):
		session_hash = enc.generate_hash(self.user.session_token)
		self.response.headers.add_header('Set-Cookie', self.create_cookie('_auth_',self.user.key.urlsafe()))
		self.response.headers.add_header('Set-Cookie', self.create_cookie('_term_',session_hash))
		
	def create_cookie(self, name, value):
		expires = datetime.datetime.now() + datetime.timedelta(days=14)
		date = expires.strftime('%a, %d %b %Y %H:%M:%S')
		cookie = ' %s=%s, expires=%s, path=/, domain=.showtown.co;' %(name, value, date)
		return cookie
		

app = webapp2.WSGIApplication([
    ('/login_handler', Login)

], debug=True)