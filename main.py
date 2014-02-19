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
    genres = [{'name':'Alternative', 'arg':'alt'}, {'name':'Blues', 'arg':'blues'}, {'name':'Classical', 'arg':'classical'}]
    template_values = {'genres':genres}
    self.render('index.html', template_values)

class TrendingHandler(views.Template):
    def get(self):
  		template_values = {}
  		self.render('trending.html', template_values)
		
class VenuesHandler(views.Template):
    def get(self):
  		template_values = {}
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
        		
class SignupVebueHandler(views.Template):
    def get(self):
  		template_values = {}
  		self.render('signup_venue.html', template_values)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/trending', TrendingHandler),
    ('/venues', VenuesHandler),
    ('/faq', FaqHandler),
    ('/privacy', PrivacyHandler),
    ('/terms', TermsHandler),
    ('/signup_fan', SignupFanHandler),
    ('/signup_musician', SignupMusicianHandler),
    ('/signup_venue', SignupVebueHandler)
    
], debug=True)
