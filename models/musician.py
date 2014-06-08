from google.appengine.ext import ndb
from address import Address
from videos import Videos
import logging

class Musician(ndb.Model):
	user_key = ndb.KeyProperty(required = True)
	user_name = ndb.StringProperty()
	band_name = ndb.StringProperty()
	band_genre = ndb.StringProperty(repeated = True)
	email = ndb.StringProperty()
	address = ndb.StructuredProperty(Address, repeated=True)
	musician_state = ndb.ComputedProperty(lambda self: self.address[0].state)
	musician_city = ndb.ComputedProperty(lambda self: self.address[0].city)
	profile_pic = ndb.BlobProperty()
	num_of_members = ndb.IntegerProperty()
	bio = ndb.TextProperty()
	DOB = ndb.DateProperty()
	facebook = ndb.StringProperty()
	twitter = ndb.StringProperty()
	sound_cloud = ndb.StringProperty()
	video_hosting_page = ndb.StringProperty()
	current_rank = ndb.IntegerProperty()
	state_rank = ndb.IntegerProperty()
	musician_stats = ndb.JsonProperty(default ={})
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
		except Exception as e:
			logging.exception(e)
			return None
			
	@classmethod
	def filter_by_state(cls, state):
		return cls.query(cls.musician_state == state).order(cls.state_rank).fetch()
		
	@classmethod
	def fetch_distinct_states(cls):
		return cls.query(projection=[cls.musician_state], distinct=True).fetch()

	@classmethod
	def fetch_distinct_cities(cls, state):
		return cls.query(cls.musician_state == state, projection=[cls.musician_city], distinct=True).fetch()


	@classmethod
	def fetch_all(cls):
		return cls.query().fetch(100000)

	@classmethod
	def fetch_by_genre_state(cls, genre, state):
		return cls.query(cls.band_genre == genre, cls.musician_state == state).order(cls.current_rank).fetch()

	@classmethod
	def count_by_state(cls, state):
		return cls.query(cls.musician_state == state).count()


	@classmethod
	def filter_by_popularity(cls,qry,popularity):
		return cls.query(cls.current_rank <= popularity).fetch()
		
