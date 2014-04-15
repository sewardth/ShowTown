from google.appengine.ext import ndb

class Videos(ndb.Model):
	acc_key = ndb.KeyProperty()
	musician_key = ndb.KeyProperty()
	musician_name = ndb.StringProperty()
	embed_link = ndb.StringProperty()
	genre_tag = ndb.StringProperty()
	video_title = ndb.StringProperty()
	featured = ndb.BooleanProperty(default = False)
	wins = ndb.IntegerProperty()
	losses = ndb.IntegerProperty()
	draws = ndb.IntegerProperty()
	video_added = ndb.DateTimeProperty(auto_now_add = True)
	
	@classmethod
	def query_by_account(cls, acc_key):
		return cls.query(cls.acc_key == acc_key).fetch()
		
	@classmethod
	def fetch_featured(cls):
		return cls.query(cls.featured == True).fetch(100)
		
	@classmethod
	def fetch_by_musician(cls, musician_key):
		return cls.query(cls.musician_key == musician_key).fetch()
		