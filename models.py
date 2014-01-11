from google.appengine.ext import db

class Contact(db.Model):
	name = db.StringProperty()
	email_address = db.EmailProperty()
	message = db.TextProperty()
	submission_date = db.DateTimeProperty(auto_now_add = True)