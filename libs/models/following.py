from google.appengine.ext import ndb

class Following(ndb.Model):
	followed_entity_key = ndb.KeyProperty()
	follower_key = ndb.KeyProperty()
	followed_date = ndb.DateTimeProperty(auto_now_add = True)
	
	
	@classmethod
	def get_by_keys(cls, user_key, followed_key):
		return cls.query(cls.followed_entity_key == followed_key, cls.follower_key == user_key).get()
		
	@classmethod
	def fetch_by_user(cls, user_key):
		return cls.query(cls.follower_key == user_key).fetch(100)
		
	@classmethod
	def fetch_by_followed_key(cls, followed_key):
		return cls.query(cls.followed_entity_key == followed_key).fetch(10000)
		
	@classmethod
	def fetch_followers_count(cls, followed_keys):
		return cls.query(cls.followed_entity_key.IN(followed_keys)).fetch()