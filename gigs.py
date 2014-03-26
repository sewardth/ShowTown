import views, webapp2, models, time
from helpers.form_validation import Validate
from datetime import datetime
from google.appengine.ext import ndb


class VenueAddEditGigHandler(views.Template):
	def get(self):
		user = self.user_check()
		if user.account_type != 'venue':
			self.response.out.write('Not Authorized')
		else:
			try: #Verifys user is owner of specified gig
				gig_key = ndb.Key(urlsafe=self.request.get('id'))
				check_key = models.events.Event.query_by_key(gig_key)
				if user.key == check_key.venue_account_key:
					template_values = {'add':0, 'gig':check_key}
					self.render('venue_add_edit_gig.html', template_values) 
			
				else:
					self.response.out.write('Not Authorized')
		
			except: #Else displays blank form
				template_values = {'add':1}
				self.render('venue_add_edit_gig.html', template_values)

	def post(self):
		user = self.user_check()
		venue = models.venue.Venue.query_by_account(user.key)
		
		host_name = self.request.get('host_name')
		event_date = Validate.validate_dob(self.request.get('event_date'))
		start_time = self.request.get('start_time')
		end_time = self.request.get('end_time')
		compensation = self.request.get('compensation')
		locality = self.request.get('locality')
		description = self.request.get('description')
		
		gig = models.events.Event(venue_key = venue.key,
									venue_account_key = user.key,
									venue = venue.venue_name,
									gig_name = host_name,
									event_date = event_date,
									start_time = start_time,
									end_time = end_time,
									compensation = compensation,
									locality = locality,
									description = description).put()
		
		time.sleep(.5)							
		self.redirect('/venue_profile')
	

class DeleteGigHandler(views.Template):
	def get(self):
		user = self.user_check()
		gig_key = ndb.Key(urlsafe=self.request.get('id'))
		check_key = models.events.Event.query_by_key(gig_key)
		if user.key == check_key.venue_account_key:
			gig_key.delete()
			time.sleep(.2)
			self.redirect('/venue_profile')
		else:
			self.response.out.write('Not Authorized')
		
		
		
app = webapp2.WSGIApplication([
   
    ('/venue_add_edit_gig.*', VenueAddEditGigHandler),
	('/delete_gig.*', DeleteGigHandler)


], debug=True)