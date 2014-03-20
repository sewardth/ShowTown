from google.appengine.ext import ndb

class Videos(ndb.Model):
	embed_link = ndb.StringProperty()
	genre_tag = ndb.StringProperty()
	video_title = ndb.StringProperty()
	featured = ndb.BooleanProperty(default = False)