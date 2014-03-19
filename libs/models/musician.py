from google.appengine.ext import ndb
from address import Address
from videos import Videos

class Musician(ndb.Model):
	user_key = ndb.KeyProperty()
	user_name = ndb.StringProperty()
	band_name = ndb.StringProperty()
	email = ndb.StringProperty()
	address = ndb.StructuredProperty(Address, repeated=True)
	submission_video = ndb.StructuredProperty(Videos, repeated = True)
	profile_pic = ndb.BlobProperty()
	num_of_members = ndb.IntegerProperty()
	bio = ndb.TextProperty()
	facebook_page = ndb.StringProperty()
	twitter_page = ndb.StringProperty()
	sound_cloud_page = ndb.StringProperty()
	youtube_page = ndb.StringProperty()
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
		return cls.query(cls.key.IN(keys)).fetch()