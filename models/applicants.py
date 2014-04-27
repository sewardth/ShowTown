from google.appengine.ext import ndb

class Applicant(ndb.Model):
	gig_key = ndb.KeyProperty()
	musician_key = ndb.KeyProperty()
	applicant_video = ndb.KeyProperty()
	video_link = ndb.StringProperty()
	applicant_status = ndb.BooleanProperty(default = True)
	performing = ndb.BooleanProperty(default = False)
	event_date = ndb.DateProperty()
	applied_date = ndb.DateTimeProperty(auto_now_add = True)
	modifed_date = ndb.DateTimeProperty(auto_now = True) 
	
	
	@classmethod
	def query_by_musician_key(cls, musician_key):
		try:
			return cls.query(cls.musician_key.IN(musician_key)).fetch()
		except:
			return None
	
	@classmethod	
	def query_by_gig(cls, gig_key):
		return cls.query(cls.gig_key == gig_key).fetch()
		
	@classmethod	#need to add date filter 	>>> "2011-06-24" > "2010-06-23" True
	def query_by_performers(cls, musician_key):
		return cls.query(cls.musician_key == musician_key, performing == True ).fetch()
		
	@classmethod
	def query_for_update(cls, gig_key, musician_key):
		return cls.query(cls.gig_key == gig_key, cls.musician_key == musician_key).get()
		
	@classmethod
	def group_by_applicant_counts(cls, gigs):
		return cls.query(cls.gig_key.IN(gigs)).fetch()