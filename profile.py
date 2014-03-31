import webapp2, json, sys, views
from google.appengine.ext import ndb
sys.path.insert(0,'libs')
import models


class FanProfileHandler(views.Template):
	def get(self):
		upcoming_shows = [{'artist':'Hoodie Allen', 'artist_href':'#', 'venue':'Andiamo', 'venue_href':'#', 'show':'Friday Night Lights', 'date':'12/13/2013', 'time':'5:30pm - 7:30pm', 'details':'Friday Night Lights is a weekly gathering where diners can enjoy soft and comfortable music with their meals.'}, 
		{'artist':'Mac Miller', 'artist_href':'#', 'venue':'Andiamo', 'venue_href':'#', 'show':'Saturday Night Jams', 'date':'12/14/2013', 'time':'10:00pm - 2:00am', 'details':'Every saturday the venue becomes a club and we like high energy music.'}]
		followed_musicians = [{'img_src':'images/_test_profile.jpg', 'name':'Transit', 'id':'0', 'liked_percent':41,
		'voted_img_src':'images/_test_profile.jpg', 'voted_name':'Sage Francis', 'voted_id':'0', 'voted_liked_percent':70},
		{'img_src':'images/_test_profile.jpg', 'name':'Mac Miller', 'id':'0', 'liked_percent':42,
		'voted_img_src':'images/_test_profile.jpg', 'voted_name':'Hoodie Allen', 'voted_id':'0', 'voted_liked_percent':61}]
		
		user = self.user_check() #returns user account info
		fan = models.fan.Fan.query_by_account(user.key) #returns fan profile info
		participation = models.voting.Voting.query_by_user(user.key)
		followed_artists = models.musician.Musician.fetch_artists(fan.following)  #returns an array of Musician objects - can parse in template using for loop.*
		
		template_values = {'following_count':len(fan.following), 'matchups_count':len(participation), 'fav_genres':'Hip-Hop/Rap, Alternative','upcoming_shows':None, 
		'followed_musicians':followed_artists, 'fan_profile':fan}
		self.render('fan_profile.html', template_values)


class FanProfileEditHandler(views.Template):
	def get(self):
		user = self.user_check() #returns user account info
		fan = models.fan.Fan.query_by_account(user.key) #returns fan profile info
		
		template_values = {'account':user, 'profile':fan}
		self.render('fan_profile_edit.html', template_values)
		
	def post(self):
		self.response.headers['Content-Type'] = "text/plain"
		self.response.out.write(self.request.body)




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
		
		template_values = {'venue_name':venue.venue_name, 'venue_type':venue.venue_type,
		'venue_address':venue.address[0].address_1  + ', ' + venue.address[0].address_2  + ' ' + venue.address[0].city  + ', ' + venue.address[0].state  + ' ' + str(venue.address[0].zip), 
		'venue_phone':venue.phone, 'venue_url':'Need field in DB',
		'venue_url_text':'Andiamoitalia.com','venue_age_limit':venue.age_limit, 'venue_capacity':venue.capacity, 'available_gigs':gigs, 'venue':venue}



		self.render('venue_profile.html', template_values)

class VenueProfileEditHandler(views.Template):
	def get(self):
		user = self.user_check()
		venue = models.venue.Venue.query_by_account(user.key)
		template_values = {'profile':venue}
		self.render('venue_profile_edit.html', template_values)
		
	def post(self):
		self.response.headers['Content-Type'] = "text/plain"
		self.response.out.write(self.request.body)

class VenueProfileApplicantsHandler(views.Template):
	def get(self):
		user = self.user_check()
		applicants_data = [{'musician_id':0, 'image_src':'images/_test_profile.jpg', 
		'musician_name':'Mac Miller', 'likes_count':'1,342', 'followers_count':'132', 'genre':'Hip-Hop/Rap',
		'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'like_percent':'73'},
		{'musician_id':0, 'image_src':'images/_test_profile.jpg', 
		'musician_name':'Hoodie Allen', 'likes_count':'1,242', 'followers_count':'122', 'genre':'Hip-Hop/Rap',
		'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'like_percent':'70'}]
		template_values = {'applicants_data':applicants_data}
		self.render('venue_profile_applicants.html', template_values)
		
	def post(self):
		self.response.headers['Content-Type'] = "text/plain"
		self.response.out.write(self.request.body)

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
		followers = models.fan.Fan.followers(musician.key)
		videos = models.videos.Videos.query_by_account(user.key)

		
		
		template_values = {'musician':musician,'musician_name':musician.band_name, 'likes_count':'1,234', 'followers_count':followers, 'genre':'Hip-Hop/Rap',
		'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'musician_dob':'March, 19th 1989',
		'trending_rank':'3','trending_category':'All Musicians', 'trending_state':'Michigan', 'img_src':'images/_test_profile.jpg',
		'bio':'Steven Markowitz[1] was born in New York City and raised in a Jewish household in Plainview, Long Island along with his brother, Daniel.[2] He started writing lyrics as a child, and would perform raps for his friends at house parties. Allen first attended the Long Island School for the Gifted, then later attended Plainview &ndash; Old Bethpage John F. Kennedy High School. Growing up, his nickname was "Hoodie."',
		'new_offers':new_offers, 'booked_gigs':booked_gigs, 'videos':videos}
		self.render('musician_profile.html', template_values)

class MusicianProfileEditHandler(views.Template):
	def get(self):
		user = self.user_check()
		musician = models.musician.Musician.query_by_account(user.key)
		
		template_values = {'account':user, 'profile':musician}
		self.render('musician_profile_edit.html', template_values)
	def post(self):
		self.response.headers['Content-Type'] = "text/plain"
		self.response.out.write(self.request.body)





app = webapp2.WSGIApplication([
    ('/fan_profile', FanProfileHandler),
    ('/fan_profile_edit', FanProfileEditHandler),
    ('/venue_profile', VenueProfileHandler),
    ('/venue_profile_edit', VenueProfileEditHandler),
    ('/venue_profile_applicants', VenueProfileApplicantsHandler),
    ('/musician_profile', MusicianProfileHandler),
    ('/musician_profile_edit', MusicianProfileEditHandler),

    
], debug=True)
