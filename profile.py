import webapp2, json, sys, views
from google.appengine.ext import ndb
sys.path.insert(0,'libs')
import models


class FanProfileHandler(views.Template):
	def get(self):
		upcoming_shows = [{'artist':'Hoodie Allen', 'artist_href':'#', 'venue':'Andiamo', 'venue_href':'#', 'show':'Friday Night Lights', 'date':'12/13/2013', 'time':'5:30pm - 7:30pm', 'details':'Friday Night Lights is a weekly gathering where diners can enjoy soft and comfortable music with their meals.'}, 
		{'artist':'Mac Miller', 'artist_href':'#', 'venue':'Andiamo', 'venue_href':'#', 'show':'Saturday Night Jams', 'date':'12/14/2013', 'time':'10:00pm - 2:00am', 'details':'Every saturday the venue becomes a club and we like high energy music.'}]

		
		user = self.user_check() #returns user account info
		fan = models.fan.Fan.query_by_account(user.key) #returns fan profile info
		participation = models.voting.Voting.query_by_user(user.key)
		followed = models.following.Following.fetch_by_user(user.key)
		followed_artists = models.musician.Musician.fetch_artists([x.followed_entity_key for x in followed])  #returns an array of Musician objects - can parse in template using for loop.*
		
		template_values = {'matchups':participation, 'fav_genres':'Hip-Hop/Rap, Alternative','upcoming_shows':None, 
		'followed_musicians':followed_artists, 'fan_profile':fan}
		self.render('fan_profile.html', template_values)





class VenueProfileHandler(views.Template):
	def get(self):
		available_gigs = [{'gig_name':'Friday Night Lights', "gig_id":'0', 'date':'12/13/2013', 'time':'5:30pm - 7:30pm', 
		'detail_list':['Equipment Required','Local Musicians Only'], 'genres':'Country, Folk, Classical', 
		'detail_description':'Friday Night Lights is a weekly gathering where diners can enjoy soft and comfortable music with their meals.', 
		'compemsation':'150', 'applicant_count':4},
		{'gig_name':'Sunday Interlude', "gig_id":'0', 'date':'12/15/2013', 'time':'12:00pm - 2:00pm', 
		'detail_list':['Local or Touring Musicians'], 'genres':'Classical', 
		'detail_description':'Looking for a talented piano player to help set the mood for our lunch crowd..', 
		'compemsation':'125', 'applicant_count':2}]
		
		user = self.user_check()
		venue = models.venue.Venue.query_by_account(user.key)
		gigs = models.events.Event.query_by_venue_key(venue.key) #retuns an array of gig objects - can parse in template using for loop.
	
		try:
			applicant_query = models.applicants.Applicant.group_by_applicant_counts([x.key for x in gigs])
			applicant_list = [x.gig_key for x in applicant_query]
			for x in gigs:
				x.applicant_count =   applicant_list.count(x.key)
		except:
			pass
			


		template_values = {'venue_name':venue.venue_name, 'venue_type':venue.venue_type,
		'venue_address':venue.address[0].address_1  + ', ' + venue.address[0].address_2  + ' ' + venue.address[0].city  + ', ' + venue.address[0].state  + ' ' + str(venue.address[0].zip), 
		'venue_phone':venue.phone, 'venue_url':'Need field in DB',
		'venue_url_text':'Andiamoitalia.com','venue_age_limit':venue.age_limit, 'venue_capacity':venue.capacity, 'available_gigs':gigs, 'venue':venue}

		self.render('venue_profile.html', template_values)



class VenueProfileApplicantsHandler(views.Template):
	def post(self):
		"""user = self.user_check()
		applicants_data = [{'musician_id':0, 'image_src':'images/_test_profile.jpg', 
		'musician_name':'Mac Miller', 'likes_count':'1,342', 'followers_count':'132', 'genre':'Hip-Hop/Rap',
		'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'like_percent':'73'},
		{'musician_id':0, 'image_src':'images/_test_profile.jpg', 
		'musician_name':'Hoodie Allen', 'likes_count':'1,242', 'followers_count':'122', 'genre':'Hip-Hop/Rap',
		'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'like_percent':'70'}]
		template_values = {'applicants_data':applicants_data}
		self.render('venue_profile_applicants.html', template_values)"""
		
		gig_id = ndb.Key(urlsafe = self.request.get('id'))
		gig = gig_id.get()
		applicants = models.applicants.Applicant.query_by_gig(gig.key)
		musicians = models.musician.Musician.fetch_artists([x.musician_key for x in applicants])
		app_data =[]
		for x in applicants:
			musician = [y for y in musicians if x.musician_key == y.key] #searches query list for selected musician.  Prevents multiple queries.
			data = x.to_dict()
			del data['gig_key'], data['event_date'], data['applied_date'], data['modifed_date']
			data['gig_key'] = gig.key.urlsafe()
			data['gig_name'] = gig.gig_name
			data['musician_key'] = data['musician_key'].urlsafe()
			data['applicant_video'] = data['applicant_video'].urlsafe()
			app_data.append(data)
			
		data = {'applicants' : app_data}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data))
	
		
			

class MusicianProfileHandler(views.Template):
	def get(self):
		new_offers = [{'venue':'Andiamo', 'venue_id':'0', 'gig_name':'Friday Night Lights', "gig_id":'0', 'date':'12/13/2013', 'time':'5:30pm - 7:30pm', 
		'detail_list':['Equipment Required','Local Musicians Only'], 'genres':'Country, Folk, Classical', 
		'detail_description':'Friday Night Lights is a weekly gathering where diners can enjoy soft and comfortable music with their meals.', 
		'compemsation':'150', 'applicant_count':4}]
		booked_gigs = [{'venue':'Andiamo', 'venue_id':'0', 'gig_name':'Sunday Interlude', "gig_id":'0', 'date':'12/15/2013', 'time':'12:00pm - 2:00pm', 
		'detail_list':['Local or Touring Musicians'], 'genres':'Classical', 
		'detail_description':'Looking for a talented piano player to help set the mood for our lunch crowd..', 
		'compemsation':'125', 'applicant_count':2}]
		
		
		user = self.user_check()
		musician = models.musician.Musician.query_by_account(user.key)
		videos = models.videos.Videos.query_by_account(user.key)
		followers = models.following.Following.fetch_by_followed_key(musician.key)
		likes = models.voting.Voting.fetch_winning_count([x.key for x in videos])

		
		
		template_values = {'musician':musician, 'likes':likes, 'followers':followers,
		'trending_rank':'3','trending_category':'All Musicians', 'trending_state':'Michigan', 
		'new_offers':new_offers, 'booked_gigs':booked_gigs, 'videos':videos}
		self.render('musician_profile.html', template_values)






app = webapp2.WSGIApplication([
    ('/fan_profile', FanProfileHandler),
    ('/venue_profile', VenueProfileHandler),
    ('/applicants_profile.*', VenueProfileApplicantsHandler),
    ('/musician_profile', MusicianProfileHandler),


    
], debug=True)
