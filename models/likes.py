from google.appengine.ext import ndb

class Likes(ndb.Model):
	user_key = ndb.KeyProperty()
	musician_key = ndb.KeyProperty()
	video_key = ndb.KeyProperty()
	like_time = ndb.DateTimeProperty(auto_now_add = True)



	@classmethod
	def count_by_video(cls,video_key):
		return cls.query(cls.vide_key == video_key).count()


	@classmethod
	def count_by_musician(cls, musician_key):
		return cls.query(cls.musician_key == musician_key).count()

	