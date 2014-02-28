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

import webapp2, views

class MainHandler(views.Template):
  def get(self):
    musicians_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'California', 'abbr':'CA'}, {'name':'Florida', 'abbr':'FL'}]
    template_values = {'musicians_states':musicians_states}
    self.render('index.html', template_values)

class TrendingHandler(views.Template):
  def get(self):
    musicians_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'California', 'abbr':'CA'}, {'name':'Florida', 'abbr':'FL'}]
    template_values = {'musicians_states':musicians_states}
    self.render('trending.html', template_values)
		
class VenuesHandler(views.Template):
  def get(self):
    venues_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'Ohio', 'abbr':'OH'}]
    template_values = {'venues_states':venues_states}
    self.render('venues.html', template_values)

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

class SignupFanHandler(views.Template):
  def get(self):
		template_values = {}
		self.render('signup_fan.html', template_values)

class SignupMusicianHandler(views.Template):
  def get(self):
		template_values = {}
		self.render('signup_musician.html', template_values)
        		
class SignupVenueHandler(views.Template):
  def get(self):
		template_values = {}
		self.render('signup_venue.html', template_values)

class SignupHandler(views.Template): 
	def post(self): 
		self.response.headers['Content-Type'] = "text/plain" 
		params = {} 
		for field in self.request.arguments():
			params[field] = self.request.get_all(field) 
		user_type = params['user_type'][0]
		if user_type == 'fan':
			pass
		elif user_type == 'musician':
			pass
		else:
			pass

        
class GetMatchUpPageDataHandler(views.Template):
  def post(self):
    self.response.headers['Content-Type'] = "text/plain"
    self.response.out.write(self.request.body)

class GetMTrendingPageDataHandler(views.Template):
  def post(self):
    self.response.headers['Content-Type'] = "text/plain"
    self.response.out.write(self.request.body)
        
class GetVenuePageDataHandler(views.Template):
  def post(self):
    self.response.headers['Content-Type'] = "text/plain"
    self.response.out.write(self.request.body)  

class FanProfileHandler(views.Template):
  def get(self):
    upcoming_shows = [{'artist':'Hoodie Allen', 'artist_href':'#', 'venue':'Andiamo', 'venue_href':'#', 'show':'Friday Night Lights', 'date':'12/13/2013', 'time':'5:30pm - 7:30pm', 'details':'Friday Night Lights is a weekly gathering where diners can enjoy soft and comfortable music with their meals.'}, 
      {'artist':'Mac Miller', 'artist_href':'#', 'venue':'Andiamo', 'venue_href':'#', 'show':'Saturday Night Jams', 'date':'12/14/2013', 'time':'10:00pm - 2:00am', 'details':'Every saturday the venue becomes a club and we like high energy music.'}]
    followed_musicians = [{'img_src':'images/_test_profile.jpg', 'name':'Transit', 'id':'0', 'liked_percent':41,
      'voted_img_src':'images/_test_profile.jpg', 'voted_name':'Sage Francis', 'voted_id':'0', 'voted_liked_percent':70},
      {'img_src':'images/_test_profile.jpg', 'name':'Mac Miller', 'id':'0', 'liked_percent':42,
      'voted_img_src':'images/_test_profile.jpg', 'voted_name':'Hoodie Allen', 'voted_id':'0', 'voted_liked_percent':61}]
    template_values = {'following_count':7, 'matchups_count':313, 'fav_genres':'Hip-Hop/Rap, Alternative','upcoming_shows':upcoming_shows, 
      'followed_musicians':followed_musicians}
    self.render('fan_profile.html', template_values)
    
class FanProfileEditHandler(views.Template):
  def get(self):
		template_values = {}
		self.render('fan_profile_edit.html', template_values)
  def post(self):
    self.response.headers['Content-Type'] = "text/plain"
    self.response.out.write(self.request.body)

class VenueProfileHandler(views.Template):
  def get(self):
    available_gigs = [{'gig_name':'Friday Night Lights', "gig_id":'0', 'date':'12/13/2013', 'time':'5:30pm - 7:30pm', 
      'detail_list':['Equipment Required','Local Musicians Only'], 'genres':'Country, Folk, Classical', 
      'detail_description':'Friday Night Lights is a weekly gathering where diners can enjoy soft and comfortable music with their meals.', 
      'compemsation':'150', 'applicant_count':4},
      {'gig_name':'Sunday Interlude', "gig_id":'0', 'date':'12/15/2013', 'time':'12:00pm - 2:00pm', 
        'detail_list':['Local or Touring Musicians'], 'genres':'Classical', 
        'detail_description':'Looking for a talented piano player to help set the mood for our lunch crowd..', 
        'compemsation':'125', 'applicant_count':2}]
    template_values = {'venue_name':'Andiamo', 'venue_type':'Restaurant', 'venue_pic_url':'images/_test_venue.jpg',
      'venue_address':'42705 Grand River Ave, Novi, MI 48375', 'venue_phone':'248-348-3839', 'venue_url':'http://andiamoitalia.com/',
      'venue_url_text':'Andiamoitalia.com','venue_age_limit':'none', 'venue_capacity':'190', 'available_gigs':available_gigs}
    self.render('venue_profile.html', template_values)

class VenueProfileEditHandler(views.Template):
  def get(self):
		template_values = {}
		self.render('venue_profile_edit.html', template_values)
  def post(self):
    self.response.headers['Content-Type'] = "text/plain"
    self.response.out.write(self.request.body)

class VenueAddEditGigHandler(views.Template):
  def get(self):

    template_values = {'add':1, 'id':'233'}
    self.render('venue_add_edit_gig.html', template_values) 
  def post(self):
    self.response.headers['Content-Type'] = "text/plain"
    self.response.out.write(self.request.body)
  
class MusicianProfileHandler(views.Template):
  def get(self):
    new_offers = [{'venue':'Andiamo', 'venue_id':'0', 'gig_name':'Friday Night Lights', "gig_id":'0', 'date':'12/13/2013', 'time':'5:30pm - 7:30pm', 
      'detail_list':['Equipment Required','Local Musicians Only'], 'genres':'Country, Folk, Classical', 
      'detail_description':'Friday Night Lights is a weekly gathering where diners can enjoy soft and comfortable music with their meals.', 
      'compemsation':'150', 'applicant_count':4}]
    booked_gigs = [{'venue':'Andiamo', 'venue_id':'0', 'gig_name':'Sunday Interlude', "gig_id":'0', 'date':'12/15/2013', 'time':'12:00pm - 2:00pm', 
        'detail_list':['Local or Touring Musicians'], 'genres':'Classical', 
        'detail_description':'Looking for a talented piano player to help set the mood for our lunch crowd..', 
        'compemsation':'125', 'applicant_count':2}]
    template_values = {'musician_name':'Hoodie Allen', 'likes_count':'1,234', 'followers_count':'211', 'genre':'Hip-Hop/Rap',
      'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'musician_dob':'March, 19th 1989',
      'trending_rank':'3','trending_category':'All Musicians', 'trending_state':'Michigan', 'img_src':'images/_test_profile.jpg',
      'bio':'Steven Markowitz[1] was born in New York City and raised in a Jewish household in Plainview, Long Island along with his brother, Daniel.[2] He started writing lyrics as a child, and would perform raps for his friends at house parties. Allen first attended the Long Island School for the Gifted, then later attended Plainview &ndash; Old Bethpage John F. Kennedy High School. Growing up, his nickname was "Hoodie."',
      'new_offers':new_offers, 'booked_gigs':booked_gigs}
    self.render('musician_profile.html', template_values)

class MusicianProfileEditHandler(views.Template):
  def get(self):
		template_values = {}
		self.render('musician_profile_edit.html', template_values)
  def post(self):
    self.response.headers['Content-Type'] = "text/plain"
    self.response.out.write(self.request.body)
                                         		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/trending', TrendingHandler),
    ('/venues', VenuesHandler),
    ('/faq', FaqHandler),
    ('/privacy', PrivacyHandler),
    ('/terms', TermsHandler),
    ('/signup_fan', SignupFanHandler),
    ('/signup_musician', SignupMusicianHandler),
    ('/signup_venue', SignupVenueHandler),
    ('/signup', SignupHandler),
    ('/get_match_up_page_data', GetMatchUpPageDataHandler),
    ('/get_trending_page_data', GetMTrendingPageDataHandler),
    ('/get_venue_page_data', GetVenuePageDataHandler),
    ('/fan_profile', FanProfileHandler),
    ('/fan_profile_edit', FanProfileEditHandler),
    ('/venue_profile', VenueProfileHandler),
    ('/venue_profile_edit', VenueProfileEditHandler),
    ('/venue_add_edit_gig', VenueAddEditGigHandler),
    ('/musician_profile', MusicianProfileHandler),
    ('/musician_profile_edit', MusicianProfileEditHandler),
    
], debug=True)
