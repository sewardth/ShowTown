import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import datetime
from login.session import Session

jinja_environment = jinja2.Environment(autoescape = True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))



class Template(webapp2.RequestHandler):	
	def PageCreator(self, page, template_values):
		self.response.headers['Content-Type'] = 'text/html'
		page = jinja_environment.get_template(page)
		user = self.user_check()
		template_values['user'] = user
		template = page.render(template_values)
		return template
	
	def render(self, page, template_values):
		pageview= self.PageCreator(page, template_values)
		self.response.out.write(pageview)
		
	def user_check(self):
		user_id = self.request.cookies.get('user')
		cookie = Session().read_cookie('user',user_id)#create cookie object / compares cookie
		if cookie != None:
			user = self.user_data(cookie)
		else:
			return None
		
	def user_data(self,user):
		pass
		
	def email_sender(self, template, **kwargs):
		pass