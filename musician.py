import webapp2, json, sys, views
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
sys.path.insert(0,'libs')
import models


class MusicianHandler(views.Template):
	def get(self):
		user = self.user_check()
		musician = ndb.Key(urlsafe = self.request.get('id')).get()

		if user:
			if musician.user_key == user.key: 
				hide_follow = True 
				user_following = False

			else:
				hide_follow = False
				user_following = models.following.Following.get_by_keys(self.user_check().key, musician.key)
		else:
			user_following = False
			hide_follow = True

		#query all videos for this artist
		videos = models.videos.Videos.fetch_by_musician(musician.key)
			

		
		template_values = {'hide':hide_follow,
						   'musician':musician, 
						   'videos':videos, 
						   'call_b':str(self.request.path), 
						   'is_following':user_following}
						   
		self.render('musician.html', template_values)
    		    		                                         		
app = webapp2.WSGIApplication([
    
    ('/musician*', MusicianHandler)
    
], debug=True)


