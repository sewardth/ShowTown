from google.appengine.ext import ndb
import views, webapp2, models

class Trending(views.Template):
	def get(self):
		musicians = models.musicians.Musician.fetch_all()
		
		



app = webapp2.WSGIApplication([
    ('/tasks/trending', Trending)

], debug=True)