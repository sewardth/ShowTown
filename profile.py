import webapp2, json, sys, views, calculations as calc
from google.appengine.ext import ndb
sys.path.insert(0,'libs')
import models


class FanProfileHandler(views.Template):
	def get(self):
		user = self.user_check() #returns user account info
		fan = models.fan.Fan.query_by_account(user.key) #returns fan profile info
		participation = models.voting.Voting.recent_by_user(user.key)
		following = models.following.Following.fetch_by_user(user.key)
		match_count = len(models.voting.Voting.query_by_user(user.key))
		
		if participation != None:
			matches = self.count_likes_participation(participation, following)
		else:
			matches = None
		
		if following != None:
			following = self.count_likes_followers(following)
		else:
			following = None

		
		template_values = {'followed_musicians':following, 'matchups':matches, 'fav_genres':'Hip-Hop/Rap, Alternative','upcoming_shows':None, 
		'fan_profile':fan, 'match_count':match_count}
		self.render('fan_profile.html', template_values)

	def count_likes_participation(self, participation, followers = False):
		musician_keys = [x.video_one_artist_key for x in participation] + [x.video_two_artist_key for x in participation]
		counts = calc.LikesCount.counts_by_musicians(musician_keys)
		
		template_data = []
		for x in participation:
			data = x.to_dict()
			data['one_win_percent'] = counts[x.video_one_artist_key]
			data['two_win_percent'] = counts[x.video_two_artist_key]
			
			if followers:
				followers_list = [y.followed_entity_key for y in followers]
				if x.video_one_artist_key in followers_list: data['one_followed'] = True
				if x.video_two_artist_key in followers_list: data['two_followed'] = True
			template_data.append(data)
		return template_data
		
		
	
	def count_likes_followers(self, followed):
		musicians = models.musician.Musician.fetch_artists([x.followed_entity_key for x in followed])
		counts = calc.LikesCount.counts_by_musicians([x.key for x in musicians])
		print counts
		
		template_data = []
		for x in musicians:
			data = x.to_dict()
			data['win_percent'] = counts[x.key]
			data['key'] = x.key
			template_data.append(data)
		return template_data
			
			
		
		
	
	
	
	


class VenueProfileHandler(views.Template):
	def get(self):
		
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
		if likes != None:
			matches = models.voting.Voting.fetch_votes_musicians([musician.key])
			total_matches = [x.video_one for x in matches] + [x.video_two for x in matches]
			wins = [x.voter_choice for x in likes]
			for x in videos:
				x.total_matchups = total_matches.count(x.key)
				x.likes =  wins.count(x.key)
				if x.total_matchups and x.likes != 0:
					x.win_percent = format((float(x.likes) / x.total_matchups)*100, '.0f')
				else:
					x.win_percent = '0'
		
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
