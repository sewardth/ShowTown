from google.appengine.ext import ndb

class Voting(ndb.Model):
	voter_acc_key = ndb.KeyProperty()
	voter_type = ndb.StringProperty()
	video_one = ndb.KeyProperty()
	video_one_artist_key = ndb.KeyProperty()
	video_two = ndb.KeyProperty()
	video_two_artist_key = ndb.KeyProperty()
	voter_choice = ndb.KeyProperty()
	video_set_check = ndb.KeyProperty(repeated = True)
	voter_ip = ndb.StringProperty()
	vote_time = ndb.DateTimeProperty(auto_now_add = True)
	
	
	@classmethod
	def query_by_user(cls, acc_key):
		return cls.query(cls.voter_acc_key == acc_key).fetch(2000)