from google.appengine.ext import ndb

class Account(ndb.Model):
	password = ndb.StringProperty()
	email = ndb.StringProperty()
	session_token = ndb.StringProperty()
	facebook_token = ndb.StringProperty()
	google_token = ndb.StringProperty()
	twitter_token = ndb.StringProperty()
	known_ip_addresses = ndb.StringProperty(repeated=True)
	account_type = ndb.StringProperty()
	verified = ndb.BooleanProperty(default = False)
	iniatied_reset = ndb.BooleanProperty(default = False)
	account_created = ndb.DateTimeProperty(auto_now_add = True)
	latest_update = ndb.DateTimeProperty(auto_now = True)
	
	
	@classmethod
	def query_by_email(cls, email):
		return cls.query(cls.email == email).get()
	
	
	@classmethod
	def query_by_key(cls, key):
		return cls.query(cls._key == key).get()