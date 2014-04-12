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
			return False
	
	@staticmethod	
	def validate_dob(dob):
		try:
			date = datetime.strptime(dob, '%m/%d/%Y').date()
			return date
		except:
			return False
	
	@staticmethod
	def validate_time(time):
		try:
			t = time.strptime(time, '%H:%M')
			time = time.strftime('%H:%M', t)
			return time
		except:
			return False
		
	@staticmethod	
	def validate_passwords(password, conf_password):
		if password == '':
			return False
			
		elif password != conf_password:
			return False
			
		else:
			password = pwd.Passwords.generate_hash(password)
			return password
		
	
	@staticmethod	
	def verify_link(link, source):
		if len(link)>0:
			try:
				r = urlfetch.fetch(link)
				if source not in link:
					return False	
				else:
					return link
			except:
				return False
		else:
			return link
	
	@staticmethod		
	def get_video(link):
		if link == '':
			return None
		else:
			try:
				video = lassie.fetch(link)
				if 'embed' in link:
					video_data = {'embed_link': link,
								  'title': video['title']}
				else:
					video_data = {'embed_link' : video['videos'][1]['src'],
					             'title' : video['title']}
				return video_data
			except:
				return False