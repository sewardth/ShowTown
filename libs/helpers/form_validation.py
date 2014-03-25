import lassie, requests, webapp2, messages
from datetime import datetime
from google.appengine.api import urlfetch
from sessions import password as pwd
import time


class Validate(webapp2.RequestHandler):
	
	@staticmethod
	def validate_email(email):
		if '@' in email and '.' in email:
			return email
		else:
			messages.Message.warning('Not a valid email address')
	
	@staticmethod	
	def validate_dob(dob):
		try:
			date = datetime.strptime(dob, '%m/%d/%Y')
			return date
		except:
			messages.Message.warning('Wrong date format, should be MM/DD/YYYY')
	
	@staticmethod
	def validate_time(time):
		try:
			t = time.strptime(time, '%H:%M')
			time = time.strftime('%H:%M', t)
			return time
		except:
			messages.Message.warning('Wrong time format, should be HH:MM')
		
	@staticmethod	
	def validate_passwords(password, conf_password):
		if password == '':
			messages.Message.warning('Passwords cannont be blank')
			
		elif password != conf_password:
			messages.Message.warning('Passwords do not match')
			
		else:
			password = pwd.Passwords.generate_hash(password)
			return password
		
	
	@staticmethod	
	def verify_link(link, source):
		if len(link)>0:
			r = urlfetch.fetch(link)
			if source not in link:
				messages.Message.warning('Not a valid URL for source: ' + source)	
			else:
				return link
		else:
			return link
	
	@staticmethod		
	def get_video(link):
		try:
			video = lassie.fetch(link)
			if 'embed' in link:
				video_data = {'embed_link': link,
							  'title': video}
			else:
				video_data = {'embed_link' : video['videos'][1]['src'],
				             'title' : video['title']}
			return video_data
		except:
			messages.Message.warning('Not a vaild YouTube or Vimeo page URL')