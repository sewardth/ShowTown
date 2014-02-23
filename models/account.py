from google.appengine.ext import ndb

class Account(ndb.Model):
	password = ndb.StringProperty()
	session_token = ndb.StringProperty()
	facebook_token = ndb.StringProperty()
	google_token = ndb.StringProperty()
	twitter_token = ndb.StringProperty()
	known_ip_addresses = ndb.StringProperty(repeated=True)
	account_type = ndb.StringProperty()
	verified = ndb.BooleanProperty()
	account_created = ndb.DateTimeProperty(auto_now_add = True)
	latest_update = ndb.DateTimeProperty(auto_now = True)
	
	
	