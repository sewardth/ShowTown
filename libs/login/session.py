from webapp2_extras import securecookie

class Session(object):
	cookie = securecookie.SecureCookieSerializer('Az30*4-342?1Ederew4e')
	
	@classmethod	
	def create_cookie(cls, name, value):
		cookie = cls.cookie.serialize(name, value)
		return cookie
	
	@classmethod	
	def read_cookie(cls,name, value):
		cookie = cls.cookie.deserialize(name,value,max_age=172800)
		return cookie
		
	
		
		