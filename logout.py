import webapp2, sys, uuid, datetime, time, views
sys.path.insert(0,'libs')


from sessions.cookie import Cookie

	

class Logout(views.Template):
	def get(self):
		_auth_ = Cookie.create_cookie('_auth_','None')
		_term_ = Cookie.create_cookie('_term_','None')
		Cookie.set_cookie(_auth_, self.response)
		Cookie.set_cookie(_term_, self.response)
		time.sleep(.5)
		self.redirect('/')
		



app = webapp2.WSGIApplication([
    ('/logout_handler', Logout)

], debug=True)