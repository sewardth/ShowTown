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

import webapp2, views, json, models, uuid, sys
sys.path.insert(0,'libs')
import lassie, requests
from google.appengine.api import urlfetch
from datetime import datetime
from sessions import password as pwd





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
    venues_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'Ohio', 'abbr':'OH'}]
    template_values = {'venues_states':venues_states}
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
		params['ip_addr'] = list(self.request.remote_addr)
		user_type = params['user_type'][0]
		
		
		
		if user_type == 'fan':
			self.fan_creator(params)
			
		elif user_type == 'musician':
			self.musician_creator(params)
			
		else:
			self.venue_creator(params) 


	
	def account_creator(self, params):
		password = self.validate_passwords(params['password'][0], params['conf_password'][0])
		account = models.account.Account(password = password, email = params['email'][0], known_ip_addresses = params['ip_addr'], 
					      				account_type = params['user_type'][0])
		acc_key = account.put()
		return acc_key
		
		
	def validate_email(self, email):
		if '@' in email and '.' in email:
			return email
		else:
			self.error_message('Not a valid email address')
		
	def validate_dob(self, dob):
		try:
			date = datetime.strptime(dob, '%m/%d/%Y')
			return date
		except:
			self.error_message('Wrong date format, should be MM/DD/YYYY')
		
		
	def validate_passwords(self, password, conf_password):
		if password == '':
			self.error_message('Passwords cannont be blank')
			
		elif password != conf_password:
			self.error_message('Passwords do not match')
			
		else:
			password = pwd.Passwords.generate_hash(password)
			return password
		
	def check_for_user(self, email):
		q = models.account.Account.query_by_email(email)
		if q == None:
			return False
		else:
			self.error_message('User already exists as type: ' + q.account_type)
		
	def verify_link(self, link, source):
		if len(link)>0:
			r = urlfetch.fetch(link)
			if r.status_code != 200 or source not in link:
				self.error_message('Not a valid URL for source: ' + source)	
			else:
				return link
		else:
			return link
			
	def get_video(self, link):
		try:
			video = lassie.fetch(link)
			video_data = {'embed_link' : video['videos'][1]['src'],
			             'title' : video['title']}
			return video_data
		except:
			self.error_message('Not a vaild YouTube or Vimeo page URL')
			
		
	def error_message(self, error):
		raise ValueError(error)	
	
	def fan_creator(self, params):
		email = self.validate_email(params['email'][0])
		DOB = self.validate_dob(params['dob'][0])
		existing_user = self.check_for_user(params['email'][0])
		acc_key = self.account_creator(params)
		user = models.fan.Fan(user_key = acc_key, email = email, DOB = DOB, genres = params['checkboxes'])
		user.put()
		
	def musician_creator(self, params):
		email = self.validate_email(params['email'][0])
		DOB = self.validate_dob(params['dob'][0])
		submission_video = self.get_video(params['video_url'][0])
		twitter = self.verify_link(params['twitter'][0],'twitter')
		sound_cloud = self.verify_link(params['sound_cloud'][0],'soundcloud')
		#youtube_page = self.verify_link(params['youtube'][0], 'youtube')
		#facebook = self.verify_link(params['facebook'[0]], 'facebook')
		existing_user = self.check_for_user(params['email'][0])
		acc_key = self.account_creator(params)
		user = models.musician.Musician(user_key = acc_key, 
										band_name = params['musician_name'][0],
										email = params['email'][0], 
										address= [models.address.Address(city=params['city'][0],
																		 state = params['state'][0], 
																		 zip = int(params['zip'][0]))], 
										submission_video = models.videos.Videos(embed_link = submission_video['embed_link'],
																				genre_tag = params['video_genre'][0],
																				video_title = submission_video['title']),
										profile_pic = params['file_upload'][0],
										num_of_members = int(params['num_of_members'][0]),
										bio = params['bio'][0],
										#facebook_page = facebook,
										#youtube_page = youtube_page,
										twitter_page = twitter,
										sound_cloud_page = sound_cloud)
		print 'user object created'
		user.put()
		print 'user stored'
		
		
	def venue_creator(self, params):
		pass





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
    videos = [{'url':'http://www.youtube.com/embed/2KRa_FjTs2U?rel=0', 'title':'You Are Not a Robot', 'likes_count':415, 'matchup_wins_percent':73, 'featured':True},
      {'url':'http://www.youtube.com/embed/_t431MAUQlQ?rel=0', 'title':'No Interruption', 'likes_count':200, 'matchup_wins_percent':45, 'featured':False}]
    template_values = {'musician_name':'Hoodie Allen', 'likes_count':'1,234', 'followers_count':'211', 'genre':'Hip-Hop/Rap',
      'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'musician_dob':'March, 19th 1989',
      'trending_rank':'3','trending_category':'All Musicians', 'trending_state':'Michigan', 'img_src':'images/_test_profile.jpg',
      'bio':'Steven Markowitz[1] was born in New York City and raised in a Jewish household in Plainview, Long Island along with his brother, Daniel.[2] He started writing lyrics as a child, and would perform raps for his friends at house parties. Allen first attended the Long Island School for the Gifted, then later attended Plainview &ndash; Old Bethpage John F. Kennedy High School. Growing up, his nickname was "Hoodie."',
      'new_offers':new_offers, 'booked_gigs':booked_gigs, 'videos':videos}
    self.render('musician_profile.html', template_values)

class MusicianProfileEditHandler(views.Template):
  def get(self):
		template_values = {}
		self.render('musician_profile_edit.html', template_values)
  def post(self):
    self.response.headers['Content-Type'] = "text/plain"
    self.response.out.write(self.request.body)

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
    ('/signup_fan', SignupFanHandler),
    ('/signup_musician', SignupMusicianHandler),
    ('/signup_venue', SignupVenueHandler),
    ('/signup', SignupHandler),
    ('/fan_profile', FanProfileHandler),
    ('/fan_profile_edit', FanProfileEditHandler),
    ('/venue_profile', VenueProfileHandler),
    ('/venue_profile_edit', VenueProfileEditHandler),
    ('/venue_add_edit_gig', VenueAddEditGigHandler),
    ('/musician_profile', MusicianProfileHandler),
    ('/musician_profile_edit', MusicianProfileEditHandler),
    ('/musician', MusicianHandler),
    ('/venue', VenueHandler),
    
], debug=True)
