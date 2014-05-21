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

import webapp2, json, sys, views, random
sys.path.insert(0,'libs')
from helpers import static_lookups as lookup
import models


class MainHandler(views.Template):
	def get(self):
		videos = models.videos.Videos.fetch_featured()
		try:
			vids = random.sample(videos,2)
		except:
			vids = None
		
		user = self.user_check()
		if user:
			if user.account_type == 'musician': 
				pro = models.musician.Musician.query_by_account(user.key)
			else:
				pro = user
			participation = models.voting.Voting.recent_by_user(user.key)
			if participation != None and len(participation)>0:
				total_votes = models.voting.Voting.fetch_votes_musicians([x.video_one_artist_key for x in participation]+[x.video_two_artist_key for x in participation])
				total_matches = [x.video_one_artist_key for x in total_votes] + [x.video_two_artist_key for x in total_votes]
				likes = [x.voter_choice_musician_key for x in total_votes]
				user_followed = models.following.Following.fetch_by_user(user.key)
				followed = [x.followed_entity_key for x in user_followed]
				musician_data = {x.key:x.band_name for x in models.musician.Musician.fetch_artists([x.video_one_artist_key for x in participation]+[x.video_two_artist_key for x in participation])}
				for x in participation:
					data = x.to_dict()
					one_total = total_matches.count(x.video_one_artist_key)
					two_total = total_matches.count(x.video_two_artist_key)
					one_likes = likes.count(x.video_one_artist_key)
					two_likes = likes.count(x.video_two_artist_key)
					x.video_one_name = musician_data[x.video_one_artist_key]
					x.video_two_name = musician_data[x.video_two_artist_key]
					if one_likes !=0 or one_total !=0:
						x.one_win_percent = format((float(one_likes)/one_total)*100, '.0f')
					else: 
						x.one_win_percent = '0'
					if two_likes !=0 or two_total !=0:
						x.two_win_percent = format((float(two_likes)/two_total)*100, '.0f')
					else:
						x.two_win_percent ='0'
					if x.video_one_artist_key in followed or pro.key == x.video_one_artist_key: x.one_followed = True
					if x.video_two_artist_key in followed or pro.key == x.video_two_artist_key: x.two_followed = True
					
			else:
				participation = None
			
				
		else:
			participation = None

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
			genre = []
			
		template_values = {'musicians_states':json.dumps(musicians_states), 'vids': vids, 'matchups':participation, 'genres':json.dumps(genre)}			
		self.render('index.html', template_values)
					

	def post(self):
		# NOTE: we are posting genre and state.
		state = self.request.get('state_code')
		genre = self.request.get('genre_code')
		user = self.user_check()
		self.videos = models.videos.Videos.fetch_featured()
		
		try:
			random.sample(self.videos,2)

			if user:
				self.user_votes = models.voting.Voting.query_by_user(user.key)
		
				if self.user_votes != None:
					self.user_votes = [[x.video_one,x.video_two] for x in self.user_votes]
					page_vids = False
					while page_vids == False and len(self.videos)>1:
						rand_vid = random.choice(self.videos)
						page_vids = self.find_match(rand_vid)
						self.videos.remove(rand_vid)
				else:
					page_vids = random.sample(self.videos,2)
				
			else:
				page_vids = random.sample(self.videos,2)
		
			#Match musician info to video data
			musician_data = {x.key:x.band_name for x in models.musician.Musician.fetch_artists([x.musician_key for x in page_vids])}
			video_data = []
			for x in page_vids:
				data = x.to_dict()
				data['band_name'] = musician_data[x.musician_key]
				data['vid_key'] = x.key
				video_data.append(data)
			
		except:
			video_data = None
		
		
		lvideo = {'url':video_data[0]['embed_link'], 'musician_id':video_data[0]['musician_key'].urlsafe(), 'musician_name':video_data[0]['band_name'], 'song_name':video_data[0]['video_title'], 'key':video_data[0]['vid_key'].urlsafe()}
		rvideo = {'url':video_data[1]['embed_link'], 'musician_id':video_data[1]['musician_key'].urlsafe(), 'musician_name':video_data[1]['band_name'], 'song_name':video_data[1]['video_title'], 'key':video_data[1]['vid_key'].urlsafe()}
		data = {'lvideo':lvideo, 'rvideo':rvideo, 'genre_tag':video_data[0]['genre_tag']}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data)) 
		
		
	def find_match(self, rand_vid):
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
