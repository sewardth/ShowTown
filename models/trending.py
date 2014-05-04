from google.appengine.ext import ndb

class Trending(ndb.Model):
	musician_key = ndb.KeyProperty()
	points = ndb.FloatProperty()

