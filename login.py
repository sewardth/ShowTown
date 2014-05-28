import webapp2, sys, uuid, datetime, time, views, json
sys.path.insert(0,'libs')
import models
from sessions.password import Passwords as pwd
from helpers import messages
from helpers.encryption import Encryption as enc
from sessions.cookie import Cookie

class Login(views.Template):
	def post(self):
		password = self.request.get('password')
		email = self.request.get('email')
		path = self.request.get('url_path')

		self.user = models.account.Account.query_by_email(email)
    
		result = {}
		if self.user == None:
			result = {'error':'User not found.  Please check the email - ' + email}
		else:
			try:
				self.verify_password(password, self.user.password)
				session_hash = enc.generate_hash(self.user.session_token)
				_auth_ = Cookie.create_cookie('_auth_',self.user.key.urlsafe())
				_term_ = Cookie.create_cookie('_term_',session_hash)
				Cookie.set_cookie(_auth_, self.response)
				Cookie.set_cookie(_term_, self.response)
				time.sleep(.5)
			except:
				result = {'error':'Invalid password or account has not been activated'}

		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(result)) 


	def verify_password(self, password, pwhash):
		check = pwd.compare_hash(password, pwhash)
		if check == True and user.verified == True:
			self.user.session_token = str(uuid.uuid4())
			self.user.put()
		else:
			raise ValueError ('invalid password')


		

class Logout(views.Template):
	def get(self):
		_auth_ = Cookie.create_cookie('_auth_',self.user.key.urlsafe())
		_term_ = Cookie.create_cookie('_term_',session_hash)
		Cookie.set_cookie(_auth_, self.response)
		Cookie.set_cookie(_term_, self.response)
		time.sleep(.5)
		self.redirect('/')
		

app = webapp2.WSGIApplication([
    ('/login_handler', Login),
    ('/logout_handler', Logout)

], debug=True)