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
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
sys.path.insert(0,'libs')
import models





class VenuesHandler(views.Template):
	def get(self):
		curs = Cursor(urlsafe=self.request.get('cursor'))
		vens, next_curs, more = models.venue.Venue.query().fetch_page(10, start_cursor= curs)
		
		if more:
			next = next_curs.urlsafe()
		else:
			next = None
		
		venues_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'Ohio', 'abbr':'OH'}]
		template_values = {'venues_states':venues_states, 'venues':vens, 'cursor_for_next_page':next}
		self.render('venues.html', template_values)

	def post(self):
		# NOTE: we are posting venue_type, state_code, gig_offer and the cursor from a previous request or null if this is the initial one.
		curs = Cursor(urlsafe=self.request.get('cursor'))
		vens, next_curs, more = models.venue.Venue.query().fetch_page(10, start_cursor=curs)
		ven_data =[]
		for x in vens:
			data = x.to_dict()
			del data['photo'], data['latest_update'], data['user_key']
			data['venue_key'] = x.key.urlsafe()
			ven_data.append(data)
		if more and next_curs:
		      next = next_curs.urlsafe()
		else:
			next = None
	
		

		data = {'cursor_for_next_page':next, 'venue_data':ven_data}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data))


class VenueHandler(views.Template):
	def get(self):
		try:
			venue_key = ndb.Key(urlsafe=self.request.get('id'))
			data = venue_key.get()
		except:
			data = None
		template_values = {'venue':data}
		self.render('venue.html', template_values)
    		    		                                         		
app = webapp2.WSGIApplication([
    
    ('/venues', VenuesHandler),
    ('/venue', VenueHandler),
    
], debug=True)
