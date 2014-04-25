from google.appengine.ext import ndb

class Address(ndb.Model):
	city = ndb.StringProperty()
	state = ndb.StringProperty(choices = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
	          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
	          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
	          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
	          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])
	zip = ndb.IntegerProperty()
	address_1 = ndb.StringProperty()
	address_2 = ndb.StringProperty()
	
	