
class Passwords(object):
	def __init__(self, password):
		self.pepper = 'A*0-Ze4!1+23kKljhbo;2u32kla@45z#1Kl23nlc3#-)!mc'
		
	def generate_hash(self,password):
		pwhash = security.generate_password_hash(password, method='sha1', length=25, pepper=self.pepper)
		return pwhash
		
	def compare_hash(self,password,pwhash):
		test = security.check_password_hash(password,pwhash,pepper=self.pepper)
		return test
		
		
		
		
	


		


		


        