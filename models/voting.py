from google.appengine.ext import ndb
import datetime

class Voting(ndb.Model):
	voter_acc_key = ndb.KeyProperty()
	voter_type = ndb.StringProperty()
	video_one = ndb.KeyProperty()
	video_one_artist_key = ndb.KeyProperty()
	video_two = ndb.KeyProperty()
	video_two_artist_key = ndb.KeyProperty()
	voter_choice = ndb.KeyProperty()
	voter_choice_musician_key = ndb.KeyProperty()
	video_set_check = ndb.KeyProperty(repeated = True)
	voter_ip = ndb.StringProperty()
	vote_time = ndb.DateTimeProperty(auto_now_add = True)
	
	
	@classmethod
	def query_by_user(cls, acc_key):
		return cls.query(cls.voter_acc_key == acc_key).fetch(10000)
		
		
	@classmethod
	def fetch_winning_count(cls, video_list):
		return cls.query(cls.voter_choice.IN(video_list)).fetch(10000)
		
	@classmethod
	def fetch_votes_musicians(cls, artist_keys):
		return cls.query(ndb.OR(cls.video_one_artist_key.IN(artist_keys), cls.video_two_artist_key.IN(artist_keys))).fetch()
		

	@classmethod
	def recent_by_user(cls, acc_key):
		return cls.query(cls.voter_acc_key == acc_key).order(-cls.vote_time).fetch()
		
	@classmethod
	def get_by_vote(cls, user_key, video_keys):
		return cls.query(cls.voter_acc_key == user_key, cls.video_one.IN(video_keys), cls.video_two.IN(video_keys)).get()
        
	@classmethod
	def recent_trends(cls):
		return cls.query(cls.vote_time >= datetime.datetime.now() + datetime.timedelta(-30)).fetch()

	@classmethod
	def return_win_count(cls, musician_key):
		return cls.query(cls.voter_choice_musician_key == musician_key).count()

	@classmethod
	def return_matches_count(cls, musician_key):
		return cls.query(ndb.OR(cls.video_one_artist_key == musician_key, cls.video_two_artist_key == musician_key)).count()

	@classmethod
	def return_win_count_videos(cls, video_key):
		return cls.query(cls.voter_choice == video_key).count()

	@classmethod
	def return_matches_count_videos(cls, video_key):
		return cls.query(ndb.OR(cls.video_one == video_key, cls.video_two == video_key)).count()