import webapp2
from webapp2_extras import json


class Message(webapp2.RequestHandler):
	types = {'json': 'application/json',
			 'text': 'text/plain',
			 'html': 'text/html'}
	
	@classmethod
	def output(cls,message, content_type = 'text'):
		header = cls.types[content_type]
		self.response.headers['Content-Type'] = header
		
		if content_type == 'json':
			
			self.response.write(json.encode(message))
			
		else:
			self.response.out.write(message)
			
			
	@staticmethod
	def warning(message):
		raise ValueError(message)	
