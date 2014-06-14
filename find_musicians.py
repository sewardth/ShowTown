import webapp2, json, sys, views
from google.appengine.ext import ndb
sys.path.insert(0,'libs')
import models


class FindMusiciansHandler(views.Template):
  def get(self):
    states = models.musician.Musician.fetch_distinct_states()
    genres = models.videos.Videos.fetch_distinct_genres()
    states_select = sorted([x.musician_state for x in states])
    genre = sorted([x.genre_tag for x in genres])
    genre.insert(0,'All')
    states_select.insert(0,'All')
    selected_genre = self.request.get("g")
    selected_state = self.request.get("s")

    template_values = {'states':states_select, 'cities': ['All'], 'genres':genre, 
      'selected_genre':selected_genre, 'selected_state':selected_state}    
    self.render('find_musicians.html', template_values)


  def post(self):
    # NOTE: we are posting genre, popularity, distance, keywords and the cursor from a previous request or null if this is the initial one.
    genre = self.request.get('genre')
    state = self.request.get('state')
    city = self.request.get('city')

    #get all musicians
    musicians = models.musician.Musician.query()

    #filter results by state
    if state != 'All': musicians = musicians.filter(models.musician.Musician.musician_state == state)

    #filter by city
    if city != 'All': musicians = musicians.filter(models.musician.Musician.musician_city == city)

    #filter by genre
    if genre != 'All': musicians = musicians.filter(models.musician.Musician.band_genre == genre)


    musicians = musicians.fetch()

    if musicians:
        data =[]
        for x in musicians:
            d = x.to_dict()

            #delete Non JSON variables
            del d['user_key'], d['profile_pic'],d['latest_update'],d['account_created'],d['DOB'],d['address'][0]['geo_code']

            #add user key back in as urlsafe
            d['key']= x.key.urlsafe()

            data.append(d)
        data = {'musicians':data, 'error':''}

    else:
        data = {'musicians':'','error':'No matches found for given parameters'}
    


    self.response.headers['Content-Type'] = 'application/json' 
    self.response.out.write(json.dumps(data))    	


app = webapp2.WSGIApplication([
    
    ('/find_musicians*', FindMusiciansHandler)
    
], debug=True)


