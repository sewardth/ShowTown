import webapp2, time, sys, views
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
sys.path.insert(0,'libs')
import models


class FollowHandler(views.Template):
	def get(self):
		to_follow = ndb.Key(urlsafe = self.request.get('id'))
		call_back = self.request.get('call_b')
		result = self.request.get('result')
		user = self.user_check()
		
		if result == 'f':
			follow = models.following.Following(followed_entity_key = to_follow,
												follower_key = user.key).put()
		else:
			record = models.following.Following.get_by_keys(user.key, to_follow)
			record.key.delete()
		time.sleep(.5)
		self.redirect(call_back)
	

    		    		                                         		
app = webapp2.WSGIApplication([
    
    ('/follow*', FollowHandler)
    
], debug=True)
