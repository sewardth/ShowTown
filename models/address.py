from google.appengine.ext import ndb

class Address(ndb.Model):
	city = ndb.StringProperty()
	state = ndb.StringProperty()
	zip = ndb.IntegerProperty()
	
	