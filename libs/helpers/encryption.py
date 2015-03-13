from webapp2_extras import security

class Encryption(object):
	pepper = '#'
	
	@classmethod
	def generate_hash(cls,value):
		pwhash = security.generate_password_hash(value, method='sha1', length=25, pepper=cls.pepper)
		return pwhash
		
	@classmethod
	def compare_hash(cls,value,valhash):
		test = security.check_password_hash(value,valhash,pepper=cls.pepper)
		return test
		