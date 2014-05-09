from google.appengine.ext import ndb

class Trending(ndb.Model):
	musician_key = ndb.KeyProperty()
	likes_rank = ndb.IntegerProperty()
	win_rank = ndb.IntegerProperty()
	following_rank = ndb.IntegerProperty()
	total = ndb.ComputedProperty(lambda self: ((self.likes_rank+self.win_rank+self.following_rank)/3))


	@classmethod
	def return_by_rank(musician_keys):
		return cls.query(cls.musician_key.IN(musician_keys)).order(cls.total).fetch()

