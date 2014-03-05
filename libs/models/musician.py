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