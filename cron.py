import webapp2
import models, views
from google.appengine.ext import db

class MainHandler(views.Template):
	def get(self):
	



class closecomp(views.Template):
	def get(self):





app = webapp2.WSGIApplication([
    ('/taskslist/leaderupdate', MainHandler),
	('/taskslist/closecomp', closecomp)

    


], debug=True)