import views, webapp2, models, time, json
from helpers.form_validation import Validate
from datetime import datetime
from google.appengine.ext import ndb


class VenueAddEditGigHandler(views.Template):
	def render_errors(self, template_values):
		self.render('venue_add_edit_gig.html', template_values)
		
	def get(self):
		user = self.user_check()
		if user.account_type != 'venue':
			self.response.out.write('Not Authorized')
		else:
			try: #Verifys user is owner of specified gig
				gig_key = ndb.Key(urlsafe=self.request.get('id'))
				check_key = models.events.Event.query_by_key(gig_key) 

			
				if user.key == check_key.venue_account_key:
					template_values = {'add':0,
									   'gig_name': check_key.gig_name,
									   'event_date':check_key.event_date.strftime('%m/%d/%Y'),
									   'start_time_hour':check_key.start_time.strftime('%I'),
									   'start_time_minutes':check_key.start_time.strftime('%M'),
									   'start_time_am_pm': check_key.start_time.strftime('%p'),
									   'end_time_hour':check_key.end_time.strftime('%I'),
									   'end_time_minutes':check_key.end_time.strftime('%M'),
									   'end_time_am_pm': check_key.end_time.strftime('%p'),
									   'compensation':check_key.compensation,
									   'equipment':check_key.equipment,
									   'locality':check_key.locality,
									   'description':check_key.description,
									   'gig':check_key}
				
					self.render('venue_add_edit_gig.html', template_values) 
		
				else:
					self.response.out.write('Not Authorized')
		
			except: #Else displays blank form
				template_values = {'add':1,
								   'gig_name': '',
								   'event_date':'',
								   'start_time_hour':'',
								   'start_time_minutes':'',
								   'start_time_am_pm':'',
								   'end_time_hour':'',
								   'end_time_minutes':'',
								   'end_time_am_pm': '',
								   'compensation':'',
								   'equipment':'',
								   'locality':'',
								   'description':''}
								
								
				self.render('venue_add_edit_gig.html', template_values)

	def post(self):
		user = self.user_check()
		venue = models.venue.Venue.query_by_account(user.key)
		params = {} 
		for field in self.request.arguments():
			params[field] = self.request.get(field)
		if user.key == venue.user_key:
			gig_name = self.request.get('gig_name')
			event_date = Validate.validate_dob(self.request.get('event_date'))
			start_time_hour = self.request.get('start_time_hour')
			start_time_minutes = self.request.get('start_time_minutes')
			start_time_am_pm = self.request.get('start_time_am_pm')
			end_time_hour = self.request.get('end_time_hour')
			end_time_minutes = self.request.get('end_time_minutes')
			end_time_am_pm = self.request.get('end_time_am_pm')
			compensation = self.request.get('compensation')
			locality = self.request.get('locality')
			description = self.request.get('description')
			
			template_values={}
			#error checks
			if event_date == False: template_values['date_error'] = 'Not a valid date format.  Must be MM/DD/YYYY'
			validation = [event_date]
			
			if False in validation:
				for x in params:
					template_values[x] = params[x]
				self.render_errors(template_values)
			else:
				start_time_date = '%s %s %s %s' %(self.request.get('event_date'), start_time_hour, start_time_minutes, start_time_am_pm)
				end_time_date = '%s %s %s %s' %(self.request.get('event_date'), end_time_hour, end_time_minutes, end_time_am_pm)

				try:
					gig_key = ndb.Key(urlsafe=self.request.get('id'))
					gig = gig_key.get()
					gig.venue = venue.venue_name
					gig.gig_name = gig_name
					gig.event_date = event_date
					gig.start_time = datetime.strptime(start_time_date,'%m/%d/%Y %I %M %p')
					gig.end_time = datetime.strptime(end_time_date,'%m/%d/%Y %I %M %p')
					gig.compensation = compensation
					gig.locality = locality
					gig.description = description
					gig.put()
			
				except:
					gig = models.events.Event(venue_key = venue.key,
												venue_account_key = user.key,
												venue = venue.venue_name,
												gig_name = gig_name,
												event_date = event_date,
												start_time = datetime.strptime(start_time_date,'%m/%d/%Y %I %M %p'),
												end_time = datetime.strptime(end_time_date,'%m/%d/%Y %I %M %p'),
												compensation = compensation,
												locality = locality,
												description = description).put()
		
				time.sleep(.5)							
				self.redirect('/venue_profile')
		else:
			self.response.out.write('Not Authorized')

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
		
class AvailableGigsHandler(views.Template):
	def post(self):
		venue_id = ndb.Key(urlsafe=self.request.get('id'))
		profile = venue_id.get()
		gigs = models.events.Event.query_by_venue_key(venue_id)
		gig_data =[]
		for x in gigs:
			data = x.to_dict()
			del data['venue_key'], data['venue_account_key'], data['event_date'], data['start_time'], data['end_time'], data['created']
			data['gig_key'] = x.key.urlsafe()
			data['event_date'] = str(x.event_date.strftime('%m/%d/%Y'))
			data['start_time'] = str(x.start_time.strftime('%I:%M%p'))
			data['end_time'] = str(x.end_time.strftime('%I:%M%p'))
			gig_data.append(data)
		
		profile = profile.to_dict()
		del profile['profile_pic'], profile['latest_update'], profile['user_key']
		
			
		data = {'venue':profile, 'gigs':gig_data}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data))
			

class ApplyWindowHandler(views.Template):
	def post(self):
		#requires musician to be logged in and id=gig_id
		user = self.user_check()
		musician = models.musician.Musician.query_by_account(user.key)
		videos = models.videos.Videos.query_by_account(user.key)
		gig_id = ndb.Key(urlsafe=self.request.get('id'))
		gig = gig_id.get()
		venue = gig.venue_key.get()
		
		
		
		gig_data = gig.to_dict()
		del gig_data['venue_key'], gig_data['venue_account_key'], gig_data['event_date'], gig_data['start_time'], gig_data['end_time'], gig_data['created']
		gig_data['gig_key'] = gig.key.urlsafe()
		gig_data['event_date'] = str(gig.event_date.strftime('%m/%d/%Y'))
		gig_data['start_time'] = str(gig.start_time.strftime('%I:%M%p'))
		gig_data['end_time'] = str(gig.end_time.strftime('%I:%M%p'))

		venue = venue.to_dict()
		del venue['profile_pic'], venue['latest_update'], venue['user_key']
		
		musician_data = musician.to_dict()
		del musician_data['user_key'], musician_data['address'], musician_data['profile_pic'], musician_data['DOB'], musician_data['latest_update'], musician_data['account_created']
		musician_data['musician_key'] = musician.key.urlsafe()
		
		video_data =[]
		for x in videos:
			data = x.to_dict()
			del data['acc_key'], data['musician_key'],data['embed_link'],data['video_added']
			data['video_key'] = x.key.urlsafe()
			video_data.append(data)

		
		data = {'venue':venue, 'gig':gig_data, 'musician':musician_data, 'videos':video_data}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data))
	


class Apply_to_Gig_Handler(views.Template):
	def post(self):
		user = self.user_check()
		musician = models.musician.Musician.query_by_account(user.key)
		gig_id = ndb.Key(urlsafe = self.request.get('id'))
		gig = gig_id.get()
		if musician.key  not in gig.applicants:
			gig.applicants.append(musician.key)
			gig.put()
			

	
app = webapp2.WSGIApplication([
   
    ('/venue_add_edit_gig.*', VenueAddEditGigHandler),
	('/delete_gig.*', DeleteGigHandler),
	('/available_gig.*', AvailableGigsHandler),
	('/apply_window_gig.*', ApplyWindowHandler),
	('/apply_to_gig.*', Apply_to_Gig_Handler)


], debug=True)