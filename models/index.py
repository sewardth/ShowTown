from google.appengine.ext import ndb

class Contact(ndb.Model):
	name = db.StringProperty()
	email_address = db.EmailProperty()
	message = db.TextProperty()
	submission_date = db.DateTimeProperty(auto_now_add = True)