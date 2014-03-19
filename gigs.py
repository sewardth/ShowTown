import views, webapp2, models
from helpers.form_validation import Validate
from datetime import datetime

class VenueAddEditGigHandler(views.Template):
	def get(self):
		template_values = {'add':1, 'id':'233'}
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
									event_date = event_date,
									start_time = start_time,
									end_time = end_time,
									compensation = compensation,
									locality = locality,
									description = description).put()
									
		self.redirect('/venue_profile')
	


		
app = webapp2.WSGIApplication([
   
    ('/venue_add_edit_gig', VenueAddEditGigHandler)


], debug=True)