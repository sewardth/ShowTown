from google.appengine.ext import ndb

class Videos(ndb.Model):
	acc_key = ndb.KeyProperty()
	musician_key = ndb.KeyProperty()
	embed_link = ndb.StringProperty()
	genre_tag = ndb.StringProperty()
	video_title = ndb.StringProperty()
	featured = ndb.BooleanProperty(default = False)
	video_stats = ndb.JsonProperty(default ={})
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
		
	@classmethod
	def filter_by_state_genre(cls, musician_keys, genre):
		return cls.query(cls.musician_key.IN(musician_keys), cls.genre_tag == genre, cls.featured == True).order(-cls.video_added).fetch()
		
	@classmethod
	def fetch_distinct_genres(cls):
		return cls.query(projection=[cls.genre_tag], distinct=True).fetch()
        
	@classmethod
	def fetch_all(cls):
		return cls.query().fetch(100000)
	
	
		