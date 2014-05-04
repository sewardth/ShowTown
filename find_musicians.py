import webapp2, json, sys, views
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
sys.path.insert(0,'libs')
import models


class FindMusiciansHandler(views.Template):
  def get(self):
    user = self.user_check()
    template_values = {}
    self.render('find_musicians.html', template_values)

  def post(self):
    # NOTE: we are posting genre, popularity, distance, keywords and the cursor from a previous request or null if this is the initial one.
    data = {'hello':'there'}
    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
    self.response.out.write(json.dumps(data))    		    		                                         		

app = webapp2.WSGIApplication([
    
    ('/find_musicians*', FindMusiciansHandler)
    
], debug=True)


