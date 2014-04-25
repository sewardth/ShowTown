from google.appengine.ext import ndb
from musician import Musician

class Fan(ndb.Model):
	user_key = ndb.KeyProperty()
	#user_name = ndb.StringProperty()
	#first_name = ndb.StringProperty()
	#last_name = ndb.StringProperty()
	email = ndb.StringProperty()
	DOB = ndb.DateProperty()
	genres = ndb.StringProperty(repeated=True)
	following = ndb.KeyProperty(repeated = True)
	latest_update = ndb.DateTimeProperty(auto_now = True)
	
	
	@classmethod
	def query_by_email(cls, email):
		return cls.query(cls.email == email)
		
	@classmethod
	def query_by_account(cls, user_key):
		return cls.query(cls.user_key == user_key).get()
		
	@classmethod
	def followers(cls, musician_key):
		try:
			return cls.query(cls.following == musician_key)
		except:
			return None
	