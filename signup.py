import webapp2, json, sys, views
sys.path.insert(0,'libs')
import lassie, requests
from google.appengine.api import urlfetch
from datetime import datetime
from helpers.form_validation import Validate as valid
from helpers import messages
import models

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
		params['ip_addr'] = [self.request.remote_addr]
		user_type = params['user_type'][0]
		
		
		
		if user_type == 'fan':
			self.fan_creator(params)
			
		elif user_type == 'musician':
			self.musician_creator(params)
			
		else:
			self.venue_creator(params) 
		
		self.redirect('/')

	def check_for_user(self, email):
		q = models.account.Account.query_by_email(email)
		if q == None:
			return False
		else:
			messages.Message.warning('User already exists as type: ' + q.account_type)
			
	
	def account_creator(self, params):
		password = valid.validate_passwords(params['password'][0], params['conf_password'][0])
		account = models.account.Account(password = password, email = params['email'][0], known_ip_addresses = params['ip_addr'], 
					      				account_type = params['user_type'][0])
		acc_key = account.put()
		return acc_key
	
	
	def fan_creator(self, params):
		email = valid.validate_email(params['email'][0])
		DOB = valid.validate_dob(params['dob'][0])
		existing_user = self.check_for_user(params['email'][0])
		acc_key = self.account_creator(params)
		try:
			user = models.fan.Fan(user_key = acc_key, email = email, DOB = DOB, genres = params['checkboxes']).put()
		except:
			key = str(acc_key)
			acc_key.delete()
			messages.Message.warning('Put() failed.  Deleting ' + key)
			
		
	def musician_creator(self, params):
		email = valid.validate_email(params['email'][0])
		DOB = valid.validate_dob(params['dob'][0])
		submission_video = valid.get_video(params['video_url'][0])
		twitter = valid.verify_link(params['twitter'][0],'twitter')
		sound_cloud = valid.verify_link(params['sound_cloud'][0],'soundcloud')
		video_hosting_page = valid.verify_link(params['video_hosting_page'][0], 'YouTube/Vimeo')
		facebook = valid.verify_link(params['facebook'[0]], 'facebook')
		existing_user = self.check_for_user(params['email'][0])
		acc_key = self.account_creator(params)
		try:
			user = models.musician.Musician(user_key = acc_key, 
										band_name = params['musician_name'][0],
										email = params['email'][0], 
										address= [models.address.Address(city=params['city'][0],
																		 state = params['state'][0], 
																		 zip = int(params['zip'][0]))], 
										submission_video = [models.videos.Videos(embed_link = submission_video['embed_link'],
																				genre_tag = params['video_genre'][0],
																				video_title = submission_video['title'])],
										profile_pic = params['file_upload'][0],
										num_of_members = int(params['num_of_members'][0]),
										bio = params['bio'][0],
										facebook = facebook,
										video_hosting_page = video_hosting_page,
										twitter_page = twitter,
										sound_cloud_page = sound_cloud).put()
		except:
			key = str(acc_key)
			acc_key.delete()
			messages.Message.warning('Put() failed.  Deleting ' + key)
		
		
	def venue_creator(self, params):
		email = valid.validate_email(params['email'][0])
		existing_user = self.check_for_user(params['email'][0])
		acc_key = self.account_creator(params)
		try:
			user = models.venue.Venue(user_key = acc_key,
								  venue_name = params['venue_name'][0],
								  email = params['email'][0],
								  address = [models.address.Address(city = params['city'][0],
								             state = params['state'][0],
								             zip = int(params['zip'][0]),
								             address_1 = params['address'][0],
											 address_2 = params['address2'][0])],
								  venue_type = params['venue_type'][0],
								  age_limit = params['age_limit'][0],
								  capacity = int(params['capacity'][0]),
								  phone = params['phone1'][0],
								  photo = params['file_upload'][0]).put()
		except:
			key = str(acc_key)
			acc_key.delete()
			messages.Message.warning('Put() failed.  Deleting ' + key)


app = webapp2.WSGIApplication([
    ('/signup_fan', SignupFanHandler),
    ('/signup_musician', SignupMusicianHandler),
    ('/signup_venue', SignupVenueHandler),
    ('/signup', SignupHandler)
    
], debug=True)
