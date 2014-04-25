from google.appengine.ext import ndb

class Videos(ndb.Model):
	acc_key = ndb.KeyProperty()
	musician_key = ndb.KeyProperty()
	musician_name = ndb.StringProperty()
	musician_state = ndb.StringProperty(choices = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
	          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
	          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
	          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
	          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])
	embed_link = ndb.StringProperty()
	genre_tag = ndb.StringProperty()
	video_title = ndb.StringProperty()
	featured = ndb.BooleanProperty(default = False)
	win_percent = ndb.StringProperty(default='0')
	total_matchups = ndb.IntegerProperty(default=0)
	likes = ndb.IntegerProperty(default = 0)
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
	
	
		