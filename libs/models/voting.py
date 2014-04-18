from google.appengine.ext import ndb

class Voting(ndb.Model):
	voter_acc_key = ndb.KeyProperty()
	voter_type = ndb.StringProperty()
	video_one = ndb.KeyProperty()
	video_one_artist_key = ndb.KeyProperty()
	video_one_name = ndb.StringProperty()
	video_two = ndb.KeyProperty()
	video_two_artist_key = ndb.KeyProperty()
	video_two_name = ndb.StringProperty()
	voter_choice = ndb.KeyProperty()
	voter_choice_musician_key = ndb.KeyProperty()
	video_set_check = ndb.KeyProperty(repeated = True)
	voter_ip = ndb.StringProperty()
	one_win_percent = ndb.StringProperty(default ='0')
	two_win_percent = ndb.StringProperty(default ='0')
	one_followed = ndb.BooleanProperty(default = False)
	two_followed = ndb.BooleanProperty(default = False)
	vote_time = ndb.DateTimeProperty(auto_now_add = True)
	
	
	@classmethod
	def query_by_user(cls, acc_key):
		return cls.query(cls.voter_acc_key == acc_key).fetch(2000)
		
		
	@classmethod
	def fetch_winning_count(cls, video_list):
		return cls.query(cls.voter_choice.IN(video_list)).fetch(10000)
		
	@classmethod
	def fetch_votes_musicians(cls, artist_keys):
		return cls.query(ndb.OR(cls.video_one_artist_key.IN(artist_keys), cls.video_two_artist_key.IN(artist_keys))).fetch()
		

	@classmethod
	def recent_by_user(cls, acc_key):
		return cls.query(cls.voter_acc_key == acc_key).fetch(5)
		
	@classmethod
	def get_by_vote(cls, user_key, video_keys):
		return cls.query(cls.voter_acc_key == user_key, cls.video_one.IN(video_keys), cls.video_two.IN(video_keys)).get()