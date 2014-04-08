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
			participation = models.voting.Voting.query_by_user(user.key)
		else:
			participation = None

		musicians_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'California', 'abbr':'CA'}, {'name':'Florida', 'abbr':'FL'}]
		template_values = {'musicians_states':musicians_states, 'vids': vids, 'matchups':participation}			
		self.render('index.html', template_values)
					

	def post(self):
		# NOTE: we are posting genre and state.
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
				
		except:
			page_vids = None
		
		
		
		lvideo = {'url':page_vids[0].embed_link, 'musician_id':page_vids[0].musician_key.urlsafe(), 'musician_name':page_vids[0].musician_name, 'song_name':page_vids[0].video_title, 'key':page_vids[0].key.urlsafe()}
		rvideo = {'url':page_vids[1].embed_link, 'musician_id':page_vids[1].musician_key.urlsafe(), 'musician_name':page_vids[1].musician_name, 'song_name':page_vids[1].video_title, 'key':page_vids[1].key.urlsafe()}
		data = {'lvideo':lvideo, 'rvideo':rvideo, 'genre_tag':page_vids[0].genre_tag}
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
