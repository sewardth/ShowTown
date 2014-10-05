from google.appengine.ext import ndb
import views, webapp2, models, datetime, time, logging, csv

class Trending(views.Template):
    def get(self):
        musicians = models.musician.Musician.fetch_all()




app = webapp2.WSGIApplication([
    ('/tasks/trending/dump_data.*', Trending)

], debug=True)