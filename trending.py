

import webapp2, json, sys, views
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
sys.path.insert(0,'libs')
import models



class TrendingHandler(views.Template):
	def get(self):
		musicians_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'California', 'abbr':'CA'}, {'name':'Florida', 'abbr':'FL'}]

		template_values = {'musicians_states':musicians_states}
		self.render('trending.html', template_values)
	

	def post(self):
		# NOTE: we are posting genre, state and the cursor from a previous request or null if this is the initial one.
		curs = Cursor(urlsafe=self.request.get('cursor'))
		musicians, next_curs, more = models.musician.Musician.query().fetch_page(10, start_cursor=curs)
		followers = models.following.Following.fetch_followers_count([x.key for x in musicians])
		followers_list = [x.followed_entity_key for x in followers]
		likes = models.voting.Voting.fetch_votes_musicians([x.key for x in musicians])
		likes_list = [x.artist_one_key for x in likes]+[x.artist_two_key for x in likes]
		wins_list = [x.voter_choice for x in likes]
		
		trending_data =[]
		for x in musicians:
			data = x.to_dict()
			del data['profile_pic'], data['latest_update'], data['user_key'], data['account_created'], data['DOB']
			data['mus_key'] = x.key.urlsafe()
			data['followers_count'] = followers_list.count(x.key)
			data['likes_count'] = likes_list.count(x.key)
			data['like_percent'] = (float(wins_list.count(x.key)) /  data['likes_count'])*100
			trending_data.append(data)
		if more and next_curs:
		      next = next_curs.urlsafe()
		else:
			next = None
		
		
		data = {'cursor_for_next_page':next, 'trending_data':trending_data}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data)) 

    		    		                                         		
app = webapp2.WSGIApplication([
    ('/trending.*', TrendingHandler)

    
], debug=True)
