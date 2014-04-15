import webapp2, json, sys, views
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
sys.path.insert(0,'libs')
import models


class MusicianHandler(views.Template):
	def get(self):
		musician_key = ndb.Key(urlsafe = self.request.get('id'))
		musician = musician_key.get()
		videos = models.videos.Videos.fetch_by_musician(musician_key)
		followers = models.following.Following.fetch_by_followed_key(musician.key)
		likes = models.voting.Voting.fetch_winning_count([x.key for x in videos])
		if self.user_check(): 
			user_following = models.following.Following.get_by_keys(self.user_check().key, musician.key)
		else:
			user_following = False
	
		
		template_values = {'user':self.user_check(),'musician':musician, 'videos':videos, 'call_b':str(self.request.path), 'followers':len(followers), 'likes':len(likes), 'is_following':user_following}
		self.render('musician.html', template_values)
    		    		                                         		
app = webapp2.WSGIApplication([
    
    ('/musician*', MusicianHandler)
    
], debug=True)


