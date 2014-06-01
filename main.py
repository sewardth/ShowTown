#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2, json, sys, views, random, logging
sys.path.insert(0,'libs')
from helpers import static_lookups as lookup
import models


class MainHandler(views.Template):
	def get(self):
		videos = models.videos.Videos.fetch_featured()
		try:
			vids = random.sample(videos,2)
		except Exception as e:
			logging.exception(e)
			vids = None
		
		user = self.user_check()
		if user:
			if user.account_type == 'musician': 
				pro = models.musician.Musician.query_by_account(user.key)
			else:
				pro = user

			#pull recent votes for the user
			participation = models.voting.Voting.recent_by_user(user.key)
			if participation:
				
				#query for the musicians the user follows, then covert the keys to an array.
				user_followed = models.following.Following.fetch_by_user(user.key)
				followed = [x.followed_entity_key for x in user_followed]
				
				#query for the musicians the user has voted for and convert results to a dictionary
				musicians = models.musician.Musician.fetch_artists([x.video_one_artist_key for x in participation]+[x.video_two_artist_key for x in participation])
				musician_data = {}
				for x in musicians:
					musician_data[x.key] = x.to_dict()

				#maps participation results to musician data
				for x in participation:
					#map wins
					one_wins = musician_data[x.video_one_artist_key]['musician_stats'].get('head_to_head_wins',0)
					two_wins = musician_data[x.video_two_artist_key]['musician_stats'].get('head_to_head_wins',0)

					#maps total matchups
					one_total = musician_data[x.video_one_artist_key]['musician_stats'].get('total_matchups',0)
					two_total = musician_data[x.video_two_artist_key]['musician_stats'].get('total_matchups',0)

					#maps band names and add as object properties
					x.video_one_name = musician_data[x.video_one_artist_key]['band_name']
					x.video_two_name = musician_data[x.video_two_artist_key]['band_name']

					#calculate win % and add as object properties
					if one_wins != 0:
						x.one_win_percent = format((float(one_wins)/one_total)*100, '.0f')
					else: 
						x.one_win_percent = '0'

					if two_wins !=0:
						x.two_win_percent = format((float(two_wins)/two_total)*100, '.0f')
					else:
						x.two_win_percent ='0'

					#checks if user is already following musicians
					if x.video_one_artist_key in followed or pro.key == x.video_one_artist_key: x.one_followed = True
					if x.video_two_artist_key in followed or pro.key == x.video_two_artist_key: x.two_followed = True
					
			else:
				participation = None
			
				
		else:
			participation = None


		#queries for distinct states and genres for query selectors
		try:
			states = models.musician.Musician.fetch_distinct_states()
			genres = models.videos.Videos.fetch_distinct_genres()
			states_select = {lookup.states[x.musician_state]:x.musician_state for x in states}
			genre = {x.genre_tag:x.genre_tag for x in genres}


		except Exception as e:
			logging.exception(e)
			states_select = {}
			genre = {}
			
		template_values = {'musicians_states':json.dumps(states_select, sort_keys = True), 'vids': vids, 'matchups':participation, 'genres':json.dumps(genre, sort_keys = True)}			
		self.render('index.html', template_values)
					

	def post(self):
		# NOTE: we are posting genre and state.
		state = self.request.get('state_code')
		genre = self.request.get('genre_code')
		user = self.user_check()
		self.videos = models.videos.Videos.fetch_featured()
		

		try:
			random.sample(self.videos,2)  #Checks if more than 2 videos exist.  If not, displays error message

			if user: #Checks for previous votes by user
				self.user_votes = models.voting.Voting.query_by_user(user.key)
		
				if self.user_votes != None:
					self.user_votes = [[x.video_one,x.video_two] for x in self.user_votes] #if user has voted, create an array of votes
					page_vids = False #set initial while loop variable
					while page_vids == False and len(self.videos)>1:
						rand_vid = random.choice(self.videos) #grabs a random choice video from all videos
						page_vids = self.find_match(rand_vid) #calls find match function to find all possible unvoted matches for video
						self.videos.remove(rand_vid) #if video has appeared in all available matches, remove video from array
				else:
					page_vids = random.sample(self.videos,2) #pull any random sample
				
			else:
				page_vids = random.sample(self.videos,2) #pull any random sample
		
			#Match musician info to video data
			musician_data = {x.key:x.band_name for x in models.musician.Musician.fetch_artists([x.musician_key for x in page_vids])}
			video_data = []
			for x in page_vids:
				data = x.to_dict()
				data['band_name'] = musician_data[x.musician_key]
				data['vid_key'] = x.key
				video_data.append(data)
			
		except Exception as e:
			logging.exception(e)
			video_data = None
		
		
		lvideo = {'url':video_data[0]['embed_link'], 'musician_id':video_data[0]['musician_key'].urlsafe(), 'musician_name':video_data[0]['band_name'], 'song_name':video_data[0]['video_title'], 'key':video_data[0]['vid_key'].urlsafe()}
		rvideo = {'url':video_data[1]['embed_link'], 'musician_id':video_data[1]['musician_key'].urlsafe(), 'musician_name':video_data[1]['band_name'], 'song_name':video_data[1]['video_title'], 'key':video_data[1]['vid_key'].urlsafe()}
		data = {'lvideo':lvideo, 'rvideo':rvideo, 'genre_tag':video_data[0]['genre_tag']}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data)) 
		
		
	def find_match(self, rand_vid):
		"""Takes a random video as an argument and searches for a second video match that is unique to the logged in fan.
		   Once that video is found, it returns a two element array (random video, found match).  If not unique match is 
		   found, then it returns false."""
		   
		i =0
		
		while i < len(self.videos):
			if rand_vid.key != self.videos[i].key and ([rand_vid.key,self.videos[i].key] not in self.user_votes and [self.videos[i].key, rand_vid.key] not in self.user_votes):
				return [rand_vid,self.videos[i]]
			i+=1
		return False

class FaqHandler(views.Template):
	def get(self):
		template_values = {}
		self.render('faq.html', template_values)

class PrivacyHandler(views.Template):
	def get(self):
		template_values = {}
		self.render('privacy.html', template_values)

class TermsHandler(views.Template):
	def get(self):
		template_values = {}
		self.render('terms.html', template_values)

    		    		                                         		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/faq', FaqHandler),
    ('/privacy', PrivacyHandler),
    ('/terms', TermsHandler)
    
], debug=True)
