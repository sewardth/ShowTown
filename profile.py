import webapp2, json, sys
sys.path.insert(0,'libs')
import views, models


class FanProfileHandler(views.Template):
  def get(self):
    upcoming_shows = [{'artist':'Hoodie Allen', 'artist_href':'#', 'venue':'Andiamo', 'venue_href':'#', 'show':'Friday Night Lights', 'date':'12/13/2013', 'time':'5:30pm - 7:30pm', 'details':'Friday Night Lights is a weekly gathering where diners can enjoy soft and comfortable music with their meals.'}, 
      {'artist':'Mac Miller', 'artist_href':'#', 'venue':'Andiamo', 'venue_href':'#', 'show':'Saturday Night Jams', 'date':'12/14/2013', 'time':'10:00pm - 2:00am', 'details':'Every saturday the venue becomes a club and we like high energy music.'}]
    followed_musicians = [{'img_src':'images/_test_profile.jpg', 'name':'Transit', 'id':'0', 'liked_percent':41,
      'voted_img_src':'images/_test_profile.jpg', 'voted_name':'Sage Francis', 'voted_id':'0', 'voted_liked_percent':70},
      {'img_src':'images/_test_profile.jpg', 'name':'Mac Miller', 'id':'0', 'liked_percent':42,
      'voted_img_src':'images/_test_profile.jpg', 'voted_name':'Hoodie Allen', 'voted_id':'0', 'voted_liked_percent':61}]
    template_values = {'following_count':7, 'matchups_count':313, 'fav_genres':'Hip-Hop/Rap, Alternative','upcoming_shows':upcoming_shows, 
      'followed_musicians':followed_musicians}
    self.render('fan_profile.html', template_values)
    
class FanProfileEditHandler(views.Template):
  def get(self):
		template_values = {}
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
    template_values = {'venue_name':'Andiamo', 'venue_type':'Restaurant', 'venue_pic_url':'images/_test_venue.jpg',
      'venue_address':'42705 Grand River Ave, Novi, MI 48375', 'venue_phone':'248-348-3839', 'venue_url':'http://andiamoitalia.com/',
      'venue_url_text':'Andiamoitalia.com','venue_age_limit':'none', 'venue_capacity':'190', 'available_gigs':available_gigs}
    self.render('venue_profile.html', template_values)

class VenueProfileEditHandler(views.Template):
  def get(self):
		template_values = {}
		self.render('venue_profile_edit.html', template_values)
  def post(self):
    self.response.headers['Content-Type'] = "text/plain"
    self.response.out.write(self.request.body)

class VenueAddEditGigHandler(views.Template):
  def get(self):

    template_values = {'add':1, 'id':'233'}
    self.render('venue_add_edit_gig.html', template_values) 
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
    videos = [{'url':'http://www.youtube.com/embed/2KRa_FjTs2U?rel=0', 'title':'You Are Not a Robot', 'likes_count':415, 'matchup_wins_percent':73, 'featured':True},
      {'url':'http://www.youtube.com/embed/_t431MAUQlQ?rel=0', 'title':'No Interruption', 'likes_count':200, 'matchup_wins_percent':45, 'featured':False}]
    template_values = {'musician_name':'Hoodie Allen', 'likes_count':'1,234', 'followers_count':'211', 'genre':'Hip-Hop/Rap',
      'musician_city':'Ann Arbor', 'musician_state':'Michigan', 'musician_dob':'March, 19th 1989',
      'trending_rank':'3','trending_category':'All Musicians', 'trending_state':'Michigan', 'img_src':'images/_test_profile.jpg',
      'bio':'Steven Markowitz[1] was born in New York City and raised in a Jewish household in Plainview, Long Island along with his brother, Daniel.[2] He started writing lyrics as a child, and would perform raps for his friends at house parties. Allen first attended the Long Island School for the Gifted, then later attended Plainview &ndash; Old Bethpage John F. Kennedy High School. Growing up, his nickname was "Hoodie."',
      'new_offers':new_offers, 'booked_gigs':booked_gigs, 'videos':videos}
    self.render('musician_profile.html', template_values)

class MusicianProfileEditHandler(views.Template):
  def get(self):
		template_values = {}
		self.render('musician_profile_edit.html', template_values)
  def post(self):
    self.response.headers['Content-Type'] = "text/plain"
    self.response.out.write(self.request.body)





app = webapp2.WSGIApplication([
    ('/fan_profile', FanProfileHandler),
    ('/fan_profile_edit', FanProfileEditHandler),
    ('/venue_profile', VenueProfileHandler),
    ('/venue_profile_edit', VenueProfileEditHandler),
    ('/venue_add_edit_gig', VenueAddEditGigHandler),
    ('/musician_profile', MusicianProfileHandler),
    ('/musician_profile_edit', MusicianProfileEditHandler),

    
], debug=True)
