from google.appengine.ext import ndb

class Trending(ndb.Model):
	musician_key = ndb.KeyProperty()
	likes_rank = ndb.IntegerProperty()
	win_rank = ndb.IntegerProperty()
	following_rank = ndb.IntegerProperty()
	total = ndb.ComputedProperty(lambda self: ((self.likes_rank+self.win_rank+self.following_rank)/float(3)))
	update_time = ndb.DateTimeProperty(auto_now = True)


	@classmethod
	def return_by_rank(cls):
		return cls.query().order(cls.total).fetch()

