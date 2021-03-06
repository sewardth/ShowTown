import webapp2, json, sys, views, logging
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
sys.path.insert(0,'libs')
import models



class TrendingHandler(views.Template):
	def get(self):
		try:
			states = models.musician.Musician.fetch_distinct_states()
			genres = models.videos.Videos.fetch_distinct_genres()
			states_select = {x.musician_state:x.musician_state for x in states}
			genre = {x.genre_tag:x.genre_tag for x in genres}
			selected_state = self.request.get("s")


		except Exception as e:
			logging.exception(e)
			states_select = {}
			genre = {}

		template_values = {'musicians_states':json.dumps(states_select, sort_keys = True), 'genres':json.dumps(genre, sort_keys = True), 'selected_state':selected_state}
		self.render('trending.html', template_values)
	

	def post(self):
		genre_selection = self.request.get('genre_code')
		state_selection = self.request.get('state_code')

		#queries all musicians
		musicians = models.musician.Musician.query()

		try:

			#filter musicians by genre if selected
			if genre_selection and genre_selection != 'All':
				musicians = musicians.filter(models.musician.Musician.band_genre == genre_selection)

			#filter by state if selected and return results by state rank
			if state_selection and state_selection != 'All':
				musicians = musicians.filter(models.musician.Musician.musician_state == state_selection)
				musicians = musicians.filter(models.musician.Musician.state_rank != None)
				musicians = musicians.order(models.musician.Musician.state_rank).fetch()
			else:
				#return by overall rank
				musicians = musicians.filter(models.musician.Musician.current_rank != None)
				musicians = musicians.order(models.musician.Musician.current_rank).fetch()



			if musicians:
				trending_data =[]
				for x in musicians:
					data = x.to_dict()
					del data['profile_pic'], data['user_key'], data['DOB'],data['account_created'], data['latest_update'], data['address'][0]['geo_code']
					data['key']=x.key.urlsafe()
					trending_data.append(data)

			data = {'trending_data':trending_data, 'error':''}
			self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
			self.response.out.write(json.dumps(data)) 

		except Exception as e:
			logging.exception(e)
			response = {'error':'No matching entries based on query parameters.'}
			self.response.out.write(json.dumps(response))

    		    		                                         		
app = webapp2.WSGIApplication([
    ('/trending.*', TrendingHandler)

    
], debug=True)
