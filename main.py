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
    ('/get_venue_page_data', GetVenuePageDataHandler)
    
], debug=True)
