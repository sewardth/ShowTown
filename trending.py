

import webapp2, json, sys, views
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
from helpers import static_lookups as lookup
sys.path.insert(0,'libs')
import models



class TrendingHandler(views.Template):
	def get(self):
		try:
			states = models.musician.Musician.fetch_distinct_states()
			genres = models.videos.Videos.fetch_distinct_genres()
			musicians_states = []
			for x in states:
				data = {}
				data['abbr']= x.musician_state
				data['name']= lookup.states[x.musician_state]
				musicians_states.append(data)
			
			genre = {x.genre_tag:x.genre_tag for x in genres}


		except:
			musicians_states = []
			genres = []

		template_values = {'musicians_states':musicians_states, 'genres':genre}
		self.render('trending.html', template_values)
	

	def post(self):
		# NOTE: we are posting genre, state and the cursor from a previous request or null if this is the initial one.
		#curs = Cursor(urlsafe=self.request.get('cursor'))
		#musicians, next_curs, more = models.musician.Musician.query().fetch_page(10, start_cursor=curs)\
		genre_selection = self.request.get('genre_code')
		state_selection = self.request.get('state_code')
		musicians = models.musician.Musician.fetch_by_genre_state(genre_code, state_code)
		followers = models.following.Following.fetch_followers_count([x.key for x in musicians])
		followers_list = [x.followed_entity_key for x in followers]
		total_matchups = models.voting.Voting.fetch_votes_musicians([x.key for x in musicians])
		match_list = [x.video_one_artist_key for x in total_matchups]+[x.video_two_artist_key for x in total_matchups]
		wins_list = [x.voter_choice_musician_key for x in total_matchups]
		
		trending_data =[]
		for x in musicians:
			data = x.to_dict()
			del data['profile_pic'], data['latest_update'], data['user_key'], data['account_created'], data['DOB']
			data['mus_key'] = x.key.urlsafe()
			data['followers_count'] = followers_list.count(x.key)
			data['likes_count'] = wins_list.count(x.key)
			if data['likes_count'] != 0 and match_list.count(x.key) != 0:
				data['like_percent'] =  format((float(data['likes_count']) / match_list.count(x.key))*100, '.0f')
			else:
				data['like_percent'] = 0
			trending_data.append(data)
		#if more and next_curs:
		#      next = next_curs.urlsafe()
		#else:
		#	next = None
		
		
		data = {'trending_data':trending_data}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data)) 

    		    		                                         		
app = webapp2.WSGIApplication([
    ('/trending.*', TrendingHandler)

    
], debug=True)
