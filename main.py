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

import webapp2, json, sys, views
sys.path.insert(0,'libs')
import models





class MainHandler(views.Template):
	def get(self):
		musicians_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'California', 'abbr':'CA'}, {'name':'Florida', 'abbr':'FL'}]
		template_values = {'musicians_states':musicians_states}
		self.render('index.html', template_values)

	def post(self):
		# NOTE: we are posting genre and state.
		lvideo = {'url':'http://www.youtube.com/embed/OmEpkztK5Lw?rel=0', 'musician_id':0, 'musician_name':'Mac Miller', 'song_name':'Knock Knock'}
		rvideo = {'url':'http://www.youtube.com/embed/_t431MAUQlQ?rel=0', 'musician_id':0, 'musician_name':'Hoodie Allen', 'song_name':'No Interruption'}
		data = {'lvideo':lvideo, 'rvideo':rvideo}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data))


class TrendingHandler(views.Template):
	def get(self):
		musicians_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'California', 'abbr':'CA'}, {'name':'Florida', 'abbr':'FL'}]
		template_values = {'musicians_states':musicians_states}
		self.render('trending.html', template_values)

	def post(self):
		# NOTE: we are posting genre, state and the cursor from a previous request or null if this is the initial one.
		# results_per_page = 10
		# queryset = MyModel.objects.all()
		# cursor = self.request.get('cursor')
		# if cursor:
		#   queryset = set_cursor(queryset, cursor)
		# results = queryset[0:results_per_page] # starts at the offset marked by the cursor
		# cursor_for_next_page = get_cursor(results)
		trending_data = [{'rank':'1', 'musician_id':0, 'image_src':'images/_test_profile.jpg', 
		'musician_name':'Mac Miller', 'likes_count':'1,342', 'followers_count':'132', 'genre':'Hip-Hop/Rap',
		'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'like_percent':'73'},
		{'rank':'2', 'musician_id':0, 'image_src':'images/_test_profile.jpg', 
		'musician_name':'Hoodie Allen', 'likes_count':'1,242', 'followers_count':'122', 'genre':'Hip-Hop/Rap',
		'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'like_percent':'70'}]
		data = {'cursor_for_next_page':'base64 encoded cursor', 'trending_data':trending_data}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data)) 


class VenuesHandler(views.Template):
	def get(self):
		venues = models.venue.Venue.fetch_venues()
		
		venues_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'Ohio', 'abbr':'OH'}]
		template_values = {'venues_states':venues_states, 'venues':venues}
		self.render('venues.html', template_values)

	def post(self):
		# NOTE: we are posting venue_type, state_code, gig_offer and the cursor from a previous request or null if this is the initial one.
		# results_per_page = 10
		# queryset = MyModel.objects.all()
		# cursor = self.request.get('cursor')
		# if cursor:
		#   queryset = set_cursor(queryset, cursor)
		# results = queryset[0:results_per_page] # starts at the offset marked by the cursor
		# cursor_for_next_page = get_cursor(results)
		venue_data = [{'image_src':'images/_test_venue.jpg', 
		'venue_name':'Andiamo', 'venue_id':0, 'venue_type':'Restaurant',
		'venue_city':'Novi', 'venue_state':'Michigan', 'like_percent':'73'},
		{'image_src':'images/_test_venue.jpg', 
		'venue_name':'Ameres', 'venue_id':0, 'venue_type':'Restaurant',
		'venue_city':'Ann Arbor', 'venue_state':'Michigan', 'like_percent':'70'}]
		data = {'cursor_for_next_page':'base64 encoded cursor', 'venue_data':venue_data}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data))

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









class MusicianHandler(views.Template):
	def get(self):
		template_values = {'musician_name':'Hoodie Allen', 'likes_count':234, 'followers_count':123, 'genre':'Hip-Hop/Rap',
		'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'musician_dob':'March, 19th 1989',
		'trending_rank':'3','trending_category':'All Musicians', 'trending_state':'Michigan', 'img_src':'images/_test_profile.jpg',}
		self.render('musician.html', template_values)

class VenueHandler(views.Template):
	def get(self):
		template_values = {'venue_name':'Andiamo', 'venue_type':'Restaurant', 'venue_pic_url':'images/_test_venue.jpg',
		'venue_address':'42705 Grand River Ave, Novi, MI 48375', 'venue_phone':'248-348-3839', 'venue_url':'http://andiamoitalia.com/',
		'venue_url_text':'Andiamoitalia.com','venue_age_limit':'none', 'venue_capacity':'190',}
		self.render('venue.html', template_values)
    		    		                                         		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/trending', TrendingHandler),
    ('/venues', VenuesHandler),
    ('/faq', FaqHandler),
    ('/privacy', PrivacyHandler),
    ('/terms', TermsHandler),
    ('/musician', MusicianHandler),
    ('/venue', VenueHandler),
    
], debug=True)
