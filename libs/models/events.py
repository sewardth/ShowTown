from google.appengine.ext import ndb

class Event(ndb.Model):
	venue_key = ndb.KeyProperty()
	venue_account_key = ndb.KeyProperty()
	venue = ndb.StringProperty()
	gig_name = ndb.StringProperty()
	event_date = ndb.DateProperty()
	start_time = ndb.DateTimeProperty()
	end_time = ndb.DateTimeProperty()
	compensation = ndb.StringProperty()
	equipment = ndb.BooleanProperty()
	genres = ndb.StringProperty(repeated=True)
	locality = ndb.StringProperty()
	description = ndb.TextProperty()
	applicant_count = ndb.IntegerProperty()
	active = ndb.BooleanProperty(default = True)
	created = ndb.DateTimeProperty(auto_now_add = True)
	
	
	@classmethod
	def query_by_venue_key(cls, venue_key):
		return cls.query(cls.venue_key == venue_key).fetch()
	
	@classmethod
	def query_by_key(cls, key):
		return cls.query(cls._key == key).get()
	

			