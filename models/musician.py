from google.appengine.ext import ndb
from address import Address
from videos import Videos

class Musician(ndb.Model):
	user_key = ndb.KeyProperty()
	user_name = ndb.StringProperty()
	band_name = ndb.StringProperty()
	band_genre = ndb.StringProperty(repeated = True)
	email = ndb.StringProperty()
	address = ndb.StructuredProperty(Address, repeated=True)
	musician_state = ndb.ComputedProperty(lambda self: self.address[0].state)
	profile_pic = ndb.BlobProperty()
	num_of_members = ndb.IntegerProperty()
	bio = ndb.TextProperty()
	DOB = ndb.DateProperty()
	facebook = ndb.StringProperty()
	twitter = ndb.StringProperty()
	sound_cloud = ndb.StringProperty()
	video_hosting_page = ndb.StringProperty()
	latest_update = ndb.DateTimeProperty(auto_now = True)
	account_created = ndb.DateTimeProperty(auto_now_add = True)
	
	
	@classmethod
	def query_by_account(cls, user_key):
		return cls.query(cls.user_key == user_key).get()
		
	@classmethod
	def query_by_key(cls, key):
		return cls.query(cls._key == key).get()
		
	@classmethod
	def fetch_artists(cls, keys):
		try:
			return cls.query(cls._key.IN(keys)).fetch()
		except:
			return None
			
	@classmethod
	def filter_by_state(cls, state):
		return cls.query(cls.address[0].state == state).fetch()
		
	@classmethod
	def fetch_distinct_states(cls):
		return cls.query(projection=[cls.musician_state], distinct=True).fetch()

	@classmethod
	def fetch_all(cls):
		return cls.query().fetch(100000)
		