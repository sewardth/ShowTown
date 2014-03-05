from webapp2_extras import security

class Passwords(object):
	pepper = 'A*0-Ze4!1+23kKljhbo;2u32kla@45z#1Kl23nlc3#-)!mc'
	
	@classmethod
	def generate_hash(cls,password):
		pwhash = security.generate_password_hash(password, method='sha1', length=25, pepper=cls.pepper)
		return pwhash
		
	@classmethod
	def compare_hash(cls,password,pwhash):
		test = security.check_password_hash(password,pwhash,pepper=cls.pepper)
		return test
		
		
		
		
	


		


		


        