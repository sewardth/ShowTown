import webapp2, json, sys, views
from google.appengine.api import images
sys.path.insert(0,'libs')
import lassie, requests
from google.appengine.api import urlfetch
from datetime import datetime
from helpers.form_validation import Validate as valid
from helpers import messages
import models

class SignupFanHandler(views.Template):
  def get(self):
		template_values = {'email':[],
							'dob':[]}
		self.render('signup_fan.html', template_values)

class SignupMusicianHandler(views.Template):
  def get(self):
		template_values = {'email':[],
							'dob':[],
							'video_url':[],
							'twitter':[],
							'sound_cloud':[],
							'video_hosting_page':[],
							'facebook':[],
							'musician_name':[],
							'city':[],
							'state':[],
							'zip':[],
							'num_of_members':[],
							'bio':[]}
		self.render('signup_musician.html', template_values)



class SignupVenueHandler(views.Template):
  def get(self):
		template_values = {'venue_name':[],
							'email':[],
							'city':[],
							'state':[],
							'zip':[],
							'address':[],
							'address2':[],
							'age_limit':[],
							'capacity':[],
							'phone1':[],
							'venue_type':[]}
		self.render('signup_venue.html', template_values)
		
		

class SignupHandler(views.Template): 	
	def render_errors(self, page):
		self.render(page, self.template_values)
		
	def post(self): 
		self.response.headers['Content-Type'] = "text/plain" 
		self.template_values ={'email_error':'',
								'error':'',
								'passwords_error':'',
								'dob_error':''}
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
		
		

	def check_for_user(self, email):
		q = models.account.Account.query_by_email(email)
		if q == None:
			return True
		else:
			return False
			
	
	def account_creator(self, params, password):
		account = models.account.Account(password = password, email = params['email'][0], known_ip_addresses = params['ip_addr'], 
					      				account_type = params['user_type'][0])
		acc_key = account.put()
		return acc_key
	
	
	def fan_creator(self, params):
		email = valid.validate_email(params['email'][0])
		if params['dob'][0] != '': 
			DOB = valid.validate_dob(params['dob'][0])
		else:
			DOB = None
		existing_user = self.check_for_user(params['email'][0])
		password = valid.validate_passwords(params['password'][0], params['conf_password'][0])
		
		#Error Checks
		if email == False: self.template_values['email_error'] = 'Not a valid email address'
		if params['dob'][0] != '' and DOB == False: self.template_values['dob_error'] = 'Not a valid date format.  Must be MM/DD/YYYY'
		if existing_user == False: self.template_values['email_error'] = 'Account alredy exists. Please Login.'
		if password == False: self.template_values['passwords_error'] = 'Passwords do not match'
		validation = [email, DOB, existing_user, password]

		if False in validation:
			for x in params:
				self.template_values[x] = params[x]
			self.render_errors('signup_fan.html')
		else:
			acc_key = self.account_creator(params, password)
			try:
				user = models.fan.Fan(user_key = acc_key, email = email, DOB = DOB, genres = params['checkboxes']).put()
				self.redirect('/')
			except:
				acc_key.delete()
				self.template_values['error'] = 'Something went wrong, please try again'
				self.render_errors('signup_fan.html')
			
		
	def musician_creator(self, params):
		email = valid.validate_email(params['email'][0])
		if params['dob'][0] != '': 
			DOB = valid.validate_dob(params['dob'][0])
		else:
			DOB = None
		try:
			profile_pic = self.image_handler(params['file_upload'][0],150,150)
		except:
			profile_pic = False
		submission_video = valid.get_video(params['video_url'][0])
		twitter = valid.verify_link(params['twitter'][0],'twitter')
		sound_cloud = valid.verify_link(params['sound_cloud'][0],'soundcloud')
		if 'youtu' in params['video_hosting_page'][0]:
			video_hosting_page = valid.verify_link(params['video_hosting_page'][0], 'youtu')
		else:
			video_hosting_page = valid.verify_link(params['video_hosting_page'][0], 'vimeo')
		facebook = valid.verify_link(params['facebook'][0], 'facebook')
		existing_user = self.check_for_user(params['email'][0])
		password = valid.validate_passwords(params['password'][0], params['conf_password'][0])
		
		
		
		#Error Checks
		if email == False: self.template_values['email_error'] = 'Not a valid email address'
		if params['dob'][0] != '' and DOB == False: self.template_values['dob_error'] = 'Not a valid date format.  Must be MM/DD/YYYY'
		if existing_user == False: self.template_values['email_error'] = 'Account alredy exists. Please Login.'
		if password == False: self.template_values['passwords_error'] = 'Passwords do not match'
		if profile_pic == False: self.template_values['picture_error'] = 'Error with photo.  Please try a different format.'
		if submission_video == False: self.template_values['video_error'] = 'Not a valid YouTube or Vimeo link'
		if twitter == False: self.template_values['twitter_error'] = 'Not a valid Twitter link'
		if sound_cloud == False: self.template_values['sound_cloud_error'] = 'Not a valid Sound Cloud link'
		if video_hosting_page == False: self.template_values['video_page_error'] = 'Not a valid YouTube / Vimeo link'
		if facebook == False: self.template_values['facebook_error'] = 'Not a valid Facebook link'
		validation = [email, DOB, profile_pic, submission_video, twitter, sound_cloud, video_hosting_page, facebook, existing_user, password]
		
		if False in validation:
			self.response.out.write(validation)
			for x in params:
				self.template_values[x] = params[x]
			self.render_errors('signup_musician.html')
		else:
			acc_key = self.account_creator(params, password)
		
			#try:								
			user = models.musician.Musician(user_key = acc_key, 
							band_name = params['musician_name'][0],
							email = email, 
							address= [models.address.Address(city=params['city'][0],
															 state = params['state'][0], 
															 zip = int(params['zip'][0]))], 
						
							profile_pic = profile_pic,
							num_of_members = int(params['num_of_members'][0]),
							bio = params['bio'][0],
							DOB = DOB,
							facebook = facebook,
							video_hosting_page = video_hosting_page,
							twitter = twitter,
							sound_cloud = sound_cloud).put()
						
			video = models.videos.Videos(embed_link = submission_video['embed_link'],
														acc_key = acc_key,
														musician_key = user,
														musician_name = params['musician_name'][0],
														genre_tag = params['video_genre'][0],
														video_title = submission_video['title'],
														featured = True).put()
			self.redirect('/')
		
		"""	except:
				acc_key.delete()
				if user: user.delete()
				if video: video.delete()
				self.template_values['error'] = 'Something went wrong, please try again'
				self.render_errors('signup_musician.html') """
		
		
		
		
	def venue_creator(self, params):
		email = valid.validate_email(params['email'][0])
		existing_user = self.check_for_user(params['email'][0])
		try:
			profile_pic = self.image_handler(params['file_upload'][0],310,219)
		except:
			profile_pic = False
		password = valid.validate_passwords(params['password'][0], params['conf_password'][0])
		
		#Error Checks
		if email == False: self.template_values['email_error'] = 'Not a valid email address'
		if existing_user == False: self.template_values['email_error'] = 'Account alredy exists. Please Login.'
		if password == False: self.template_values['passwords_error'] = 'Passwords do not match'
		if profile_pic == False: self.template_values['picture_error'] = 'Error with photo.  Please try a different format.'
		validation = [email, profile_pic, existing_user, password]
		
		if False in validation:
			for x in params:
				self.template_values[x] = params[x]
			self.render_errors('signup_venue.html')
			
		else:
			acc_key = self.account_creator(params, password)
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
									  profile_pic = profile_pic).put()
									
				self.redirect('/')
			except:
				acc_key.delete()
				self.template_values['error'] = 'Something went wrong, please try again'
				self.render_errors('signup_venue.html')
	
			
	def image_handler(self, image, width, height):
		if image == '':
			return None
		else:
			image = images.Image(image_data = image)
			desired_wh_ratio = float(width) / float(height)
			wh_ratio = float(image.width) / float(image.height)

			if desired_wh_ratio > wh_ratio:
				# resize to width, then crop to heigh
				image.resize(width=width)
				image.execute_transforms()
				trim_y = (float(image.height - height) / 2) / image.height
				image.crop(0.0, 0.0, 1.0, 1 - (2 * trim_y))
			else:
				# resize to height, then crop to width
				image.resize(height=height)
				image.execute_transforms()
				trim_x = (float(image.width - width) / 2) / image.width
				image.crop(trim_x, 0.0, 1 - trim_x, 1.0)

			img = image.execute_transforms(output_encoding=images.JPEG)
			return img


app = webapp2.WSGIApplication([
    ('/signup_fan', SignupFanHandler),
    ('/signup_musician', SignupMusicianHandler),
    ('/signup_venue', SignupVenueHandler),
    ('/signup', SignupHandler)
    
], debug=True)
