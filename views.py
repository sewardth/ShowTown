import webapp2, jinja2, os, datetime, sys
from google.appengine.ext import ndb
sys.path.insert(0,'libs')
import models
from helpers.encryption import Encryption as enc
from sessions.cookie import Cookie
from jinja2 import Undefined
JINJA2_ENVIRONMENT_OPTIONS = { 'undefined' : Undefined }



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
		
			
	def _user_account(self,user):
		try:
			user = models.account.Account.query_by_key(ndb.Key(urlsafe=user))
			return user
		except:
			return None
		
	def _verify_user(self, user, session_cookie):
		test = enc.compare_hash(user.session_token, session_cookie)
		if test == True:
			return user
		else:
			return None

	def user_check(self):
		cookies = Cookie._grab_cookies(self.request)
		user = self._user_account(cookies['user'])
		if user == None:
			return None
		else:
			user = self._verify_user(user, cookies['session'])
			return user
		
		
	def email_sender(self, template, template_values):
		self.response.headers['Content-Type'] = 'text/html'
		page = jinja_environment.get_template(template)
		template = page.render(template_values)
		return template
		