import webapp2, json, sys, views
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
sys.path.insert(0,'libs')
import models


class MusicianHandler(views.Template):
	def get(self):
		user = self.user_check()
		hide_follow = False
		musician_key = ndb.Key(urlsafe = self.request.get('id'))
		musician = musician_key.get()
		if user:
			if user.account_type == 'musician':
				profile = models.musician.Musician.query_by_account(user.key)
				if musician_key == profile.key: hide_follow = True

		videos = models.videos.Videos.fetch_by_musician(musician_key)
		followers = models.following.Following.fetch_by_followed_key(musician.key)
		likes = models.voting.Voting.fetch_winning_count([x.key for x in videos])
		if likes != None:
			matches = models.voting.Voting.fetch_votes_musicians([musician.key])
			total_matches = [x.video_one for x in matches] + [x.video_two for x in matches]
			wins = [x.voter_choice for x in likes]
			for x in videos:
				x.total_matchups = total_matches.count(x.key)
				x.likes =  wins.count(x.key)
				if x.total_matchups and x.likes != 0:
					x.win_percent = format((float(x.likes) / x.total_matchups)*100, '.0f')
				else:
					x.win_percent = '0'
				
		if user: 
			user_following = models.following.Following.get_by_keys(self.user_check().key, musician.key)
		else:
			user_following = False
		
		template_values = {'hide':hide_follow,'musician':musician, 'videos':videos, 'call_b':str(self.request.path), 'followers':len(followers), 'likes':len(likes), 'is_following':user_following}
		self.render('musician.html', template_values)
    		    		                                         		
app = webapp2.WSGIApplication([
    
    ('/musician*', MusicianHandler)
    
], debug=True)


