from google.appengine.ext import ndb
from address import Address

class Musician(ndb.Model):
	user_id = ndb.KeyProperty()
	band_name = ndb.StringProperty()
	email = ndb.StringProperty()
	adress = ndb.StructuredProperty(Address, repeated=True)
	submission_video = ndb.StringProperty()
	video_two = ndb.StringProperty()
	video_three = ndb.StringProperty()
	video_four = ndb.StringProperty()
	video_five = ndb.StringProperty()
	musicians_genres = ndb.StringProperty(repeated=True)
	profile_pic = ndb.BlobProperty()
	num_of_members = ndb.IntegerProperty()
	bio = ndb.TextProperty()
	facebook_page = ndb.StringProperty()
	twitter_page = ndb.StringProperty()
	sound_cloud_page = ndb.StringProperty()
	myspace = ndb.StringProperty()
	latest_update = ndb.DateTimeProperty(auto_now = True)