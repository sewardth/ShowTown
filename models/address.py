from google.appengine.ext import ndb

class Address(ndb.Model):
	city = ndb.StringProperty()
	state = ndb.StringProperty()
	zip = ndb.IntegerProperty()
	address_1 = ndb.StringProperty()
	address_2 = ndb.StringProperty()
	geo_code = ndb.GeoPtProperty()
	
	