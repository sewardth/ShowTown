from google.appengine.ext import ndb
from address import Address

class Venue(ndb.Model):
	user_key = ndb.KeyProperty()
	venue_name = ndb.StringProperty()
	email = ndb.StringProperty()
	address = ndb.StructuredProperty(Address, repeated=True)
	venue_type = ndb.StringProperty()
	age_limit = ndb.StringProperty()
	capacity = ndb.IntegerProperty()
	latest_update = ndb.DateTimeProperty(auto_now = True)