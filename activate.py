import views, webapp2, models, time, json, logging, uuid
from helpers.encryption import Encryption as enc
from sessions.cookie import Cookie
from google.appengine.ext import ndb


class Activate(views.Template):
	def get(self):
		try:
			#finds user account and sets verifed = true and creates a session token
			user = ndb.Key(urlsafe = self.request.get('id')).get()
			self.response.out.write(user)
			user.verified = True
			user.session_token = str(uuid.uuid4())
			

			#sets login cookies so users are automatically logged in upon clicking
			session_hash = enc.generate_hash(user.session_token)
			_auth_ = Cookie.create_cookie('_auth_',user.key.urlsafe())
			_term_ = Cookie.create_cookie('_term_',session_hash)
			Cookie.set_cookie(_auth_, self.response)
			Cookie.set_cookie(_term_, self.response)
			user.put()

			#delays half a second to make sure cookies and NDB recored are set then redirects to main
			time.sleep(.5)
			self.redirect('/')

		except Exception as e:
			logging.error(e)
			self.response.out.write('An Error Occured')



app = webapp2.WSGIApplication([
   
    ('/activate.*', Activate)


], debug=True)