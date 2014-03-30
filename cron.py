import webapp2
import models, views
from google.appengine.ext import db

class MainHandler(views.Template):
	def get(self):
		videos = models.videos.Videos.fetch_featured()
		population = [[x.key,y.key] for x in videos for y in videos if y>x]





app = webapp2.WSGIApplication([
    ('/taskslist/video_population', Vids)
    


], debug=True)