import webapp2, json, sys, views
from google.appengine.ext import ndb
from helpers import static_lookups as lookup
sys.path.insert(0,'libs')
import models


class FindMusiciansHandler(views.Template):
  def get(self):
    states = models.musician.Musician.fetch_distinct_states()
    genres = models.videos.Videos.fetch_distinct_genres()
    states_select = [lookup.states[x.musician_state]for x in states]
    genre = {x.genre_tag:x.genre_tag for x in genres}
    states_select.insert(0,'All')



    template_values = {'states':sorted(states_select), 'cities': ['All'], 'genres':json.dumps(genre, sort_keys = True)}    
    self.render('find_musicians.html', template_values)


  def post(self):
    # NOTE: we are posting genre, popularity, distance, keywords and the cursor from a previous request or null if this is the initial one.
    genre = self.request.get('genre')
    popularity = self.request.get('popularity')
    state = self.request.get('state')


    data = {'hello':'there'}
    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
    self.response.out.write(json.dumps(data))    	


app = webapp2.WSGIApplication([
    
    ('/find_musicians*', FindMusiciansHandler)
    
], debug=True)


