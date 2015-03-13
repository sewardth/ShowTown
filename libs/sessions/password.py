from webapp2_extras import security

class Passwords(object):
	pepper = '#'
	
	@classmethod
	def generate_hash(cls,password):
		pwhash = security.generate_password_hash(password, method='sha1', length=25, pepper=cls.pepper)
		return pwhash
		
	@classmethod
	def compare_hash(cls,password,pwhash):
		test = security.check_password_hash(password,pwhash,pepper=cls.pepper)
		return test
		
		
		
		
	


		


		


        