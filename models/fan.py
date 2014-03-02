from google.appengine.ext import ndb

class Fan(ndb.Model):
	user_key = ndb.KeyProperty()
	#user_name = ndb.StringProperty()
	#first_name = ndb.StringProperty()
	#last_name = ndb.StringProperty()
	email = ndb.StringProperty()
	DOB = ndb.DateProperty()
	genres = ndb.StringProperty(repeated=True)
	latest_update = ndb.DateTimeProperty(auto_now = True)
	
	
	@classmethod
	def query_by_email(cls, email):
		return cls.query(email == email)
	