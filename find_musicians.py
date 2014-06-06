import webapp2, json, sys, views
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
sys.path.insert(0,'libs')
import models


class FindMusiciansHandler(views.Template):
  def get(self):
    user = self.user_check()
    template_values = {}
    self.render('find_musicians.html', template_values)


  def post(self):
    # NOTE: we are posting genre, popularity, distance, keywords and the cursor from a previous request or null if this is the initial one.
    data = {'hello':'there'}
    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
    self.response.out.write(json.dumps(data))    	
"""
    def post(self):

        genre_selection = self.request.get('genre')
        popularity_selection = self.request.get('popularity')
        state_selection = self.request.get('state')

        try:

            musicians_query = qry_all()

            if genre_selection != 'All':
                musicians_query = models.musician.Musician.filter_by_genre(musicians_query,genre_selection)

            if popularity_selection != 'All'
                musicians_query = models.musician.Musician.filter_by_popularity(musicians_query, popularity_selection)

            musicians_query = models.musician.Musician.filter_by_state(musicians_query,state_selection)

            musicians = musicians_query.order(models.musician.Musician.band_name).fetch()

            if musicians:
                trending_data =[]
                for x in musicians:
                    data = x.to_dict()
                    del data['profile_pic'], data['user_key'], data['DOB'],data['account_created'], data['latest_update']
                    data['key']=x.key.urlsafe()
                    trending_data.append(data)

            data = {'trending_data':trending_data, 'error':''}
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.out.write(json.dumps(data)) 

        except Exception as e:
            logging.exception(e)
            response = {'error':'No matching entries based on query parameters.'}
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.out.write(json.dumps(response))

    

    data = {'cursor_for_next_page':next, 'venue_data':ven_data}
    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
    self.response.out.write(json.dumps(data))  		                                         		
"""

app = webapp2.WSGIApplication([
    
    ('/find_musicians*', FindMusiciansHandler)
    
], debug=True)


