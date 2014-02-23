from webapp2_extras import securecookie

class Session(object):
	def __init__(self):
		self.cookie = securecookie.SecureCookieSerializer('Az30*4-342?1Ederew4e')
		
	def create_cookie(self, name, value):
		cookie = self.cookie.serialize(name, value)
		return cookie
		
	def read_cookie(self,name, value):
		cookie = self.cookie.deserialize(name,value,max_age=172800)
		return cookie
		
	
		
		