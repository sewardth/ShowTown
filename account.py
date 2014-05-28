import webapp2, sys, uuid, datetime, time, views, json, logging
sys.path.insert(0,'libs')
import models
from helpers.email_handler import Email
from sessions.password import Passwords as pwd
from helpers import messages
from helpers.encryption import Encryption as enc
from helpers.form_validation import Validate as valid
from sessions.cookie import Cookie
from google.appengine.ext import ndb


class Account(views.Template):
	page = 'password_reset_request.html'

	def page_refresh(self, page, template_values):
		self.render(page, template_values)

	def get(self):
		self.render(Account.page, template_values ={'response':''})

	def post(self):
		email = self.request.get('email')

		#query for account
		try:
			account = models.account.Account.query_by_email(email)
		except Exception as e:
			logging.exception(e)
			account = None

		#checks if account returns an object.  If none, refreshes page with error code.  
		if account: 
			account.iniatied_reset = True
			account.put()
			email_body = self.email_sender('email_PasswordReset.html', template_values ={'user':email, 'user_id':account.key.urlsafe()})
			Email.email('Reset your ShowTown password', email_body, email)
			self.page_refresh(Account.page, template_values ={'response':'Thank you! An email has been sent with further instructions.'})

		else:
			self.page_refresh('password_reset_request.html', template_values ={'response':'Email address not found.'})

class PasswordReset(views.Template):
	page = 'password_reset_form.html'

	def page_refresh(self, page, template_values):
		self.render(page, template_values)

	def get(self):
		#grabs user id and instantly queries for object
		try:
			account = ndb.Key(urlsafe=self.request.get('id')).get()

			if account.iniatied_reset == True:
				self.render(PasswordReset.page, template_values={'response':'', 'acct_key':account.key.urlsafe()})

			else:
				self.response.out.write('This account has not initiated a reset request.  If you believe this is an error, contact us using the instruction in the email.')

		except Exception as e:
			logging.exception(e)
			self.response.out.write('Account not found')

	def post(self):
		#grab form elements. Instantly query user object
		try:
			user = ndb.Key(urlsafe = self.request.get('acct_key')).get()
			password = self.request.get('password')
			confirm_password = self.request.get('conf_password')

			#tests to make sure initiate reset is true to prevent url manipulation.
			if user.iniatied_reset == True:
				if password == '':
					self.page_refresh(PasswordReset.page, template_values = {'response':'Password can not be blank',  'acct_key':user.key.urlsafe()})
				else:
					password = valid.validate_passwords(password, confirm_password)
					if password == False: 
						self.page_refresh(PasswordReset.page, template_values = {'response':'Passwords do not match', 'acct_key':user.key.urlsafe()})
					else:
						user.iniatied_reset = False
						user.password = password
						user.put()
						self.page_refresh(PasswordReset.page, template_values = {'response':'Reset complete.  You may login using your new credentials.'})
		
			else:
				self.response.out.write('This account has not initiated a reset request.  If you believe this is an error, contact us using the instruction in the email.')

		except Exception as e:
			logging.exception(e)
			self.response.out.write('Something went wrong.  Please contact us if this problem continues.')



app = webapp2.WSGIApplication([
    ('/account', Account),
    ('/account/reset', PasswordReset)

], debug=True)