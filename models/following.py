from google.appengine.ext import ndb
import datetime

class Following(ndb.Model):
	followed_entity_key = ndb.KeyProperty()
	follower_key = ndb.KeyProperty()
	followed_date = ndb.DateTimeProperty(auto_now_add = True)
	
	
	@classmethod
	def get_by_keys(cls, user_key, followed_key):
		return cls.query(cls.followed_entity_key == followed_key, cls.follower_key == user_key).get()
		
	@classmethod
	def fetch_by_user(cls, user_key):
		return cls.query(cls.follower_key == user_key).fetch(500)
		
	@classmethod
	def fetch_by_followed_key(cls, followed_key):
		return cls.query(cls.followed_entity_key == followed_key).fetch(10000)
		
	@classmethod
	def fetch_followers_count(cls, followed_keys):
		return cls.query(cls.followed_entity_key.IN(followed_keys)).fetch()

	@classmethod
	def recent_trends(cls):
		return cls.query(cls.followed_date >= datetime.datetime.now() + datetime.timedelta(-30)).fetch()

	@classmethod
	def return_follower_count(cls, musician_key):
		return cls.query(cls.followed_entity_key == musician_key).count()