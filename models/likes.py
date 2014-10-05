from google.appengine.ext import ndb
import datetime

class Likes(ndb.Model):
	user_key = ndb.KeyProperty()
	musician_key = ndb.KeyProperty()
	video_key = ndb.KeyProperty()
	like_time = ndb.DateTimeProperty(auto_now_add = True)



	@classmethod
	def count_by_video(cls,video_key):
		return cls.query(cls.video_key == video_key).count()


	@classmethod
	def count_by_musician(cls, musician_key):
		return cls.query(cls.musician_key == musician_key).count()

	@classmethod
	def get_existing(cls, user_key, video_key):
		return cls.query(cls.user_key == user_key, cls.video_key == video_key).get()

	@classmethod
	def recent_trends(cls):
		return cls.query(cls.like_time >= datetime.datetime.now() + datetime.timedelta(-30)).fetch()

	@classmethod
	def fetch_for_musicians(cls, musician_keys):
		return cls.query(cls.musician_key.IN(musician_keys)).fetch()