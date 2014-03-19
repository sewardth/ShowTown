from google.appengine.ext import ndb
from applicants import Applicant

class Event(ndb.Model):
	venue_key = ndb.KeyProperty()
	venue_account_key = ndb.KeyProperty()
	venue = ndb.StringProperty()
	event_date = ndb.DateProperty()
	start_time = ndb.StringProperty()
	end_time = ndb.StringProperty()
	compensation = ndb.StringProperty()
	equipment = ndb.BooleanProperty()
	genres = ndb.StringProperty(repeated=True)
	locality = ndb.StringProperty()
	description = ndb.TextProperty()
	applicants = ndb.StructuredProperty(Applicant, repeated = True)
	performers = ndb.StructuredProperty(Applicant, repeated = True)
	active = ndb.BooleanProperty(default = True)
	created = ndb.DateTimeProperty(auto_now_add = True)
	
	
	@classmethod
	def query_by_venue_key(cls, venue_key):
		return cls.query(cls.venue_key == venue_key).fetch()
		