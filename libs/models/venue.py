from google.appengine.ext import ndb
from address import Address

class Venue(ndb.Model):
	user_key = ndb.KeyProperty()
	venue_name = ndb.StringProperty()
	email = ndb.StringProperty()
	address = ndb.StructuredProperty(Address, repeated=True)
	venue_type = ndb.StringProperty()
	venue_url = ndb.StringProperty()
	phone = ndb.StringProperty()
	profile_pic = ndb.BlobProperty()
	age_limit = ndb.StringProperty()
	capacity = ndb.IntegerProperty()
	active = ndb.BooleanProperty(default = True)
	latest_update = ndb.DateTimeProperty(auto_now = True)
	
	@classmethod
	def query_by_account(cls, user_key):
		return cls.query(cls.user_key == user_key).get()
		
	@classmethod
	def fetch_venues(cls):
		return cls.query(cls.active == True).fetch(10)