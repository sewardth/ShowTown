import uuid, hmac, hashlib
import views, models
import webapp2
from webapp2_extras import security


class ID(views.Template):
	def __init__(self):
		self.key = 'FklJKjFJ978324klnkjhkk3Y$#97934242#43%#@$!OHH@#@'
		
	def encrypt_password(self,data):
		password = security.generate_password_hash(data, method='sha1', length=22, pepper=self.key)
		self.unique_id = uuid.uuid1()
		return password
		
		
	def UUID(self):
		return self.unique_id
		
	def key(self):
		return str(self.key)

		


		


        