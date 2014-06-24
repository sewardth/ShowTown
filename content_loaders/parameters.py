import webapp2, sys, views, json, logging, models
sys.path.insert(0,'libs')


class DistinctCities(views.Template):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'  
		if self.request.get('state') == 'All':
			self.response.out.write(json.dumps({'cities':['All']}))

		else:
			state = self.request.get('state')
			genre = self.request.get('genre')
			c_name = models.musician.Musician
			if genre != 'All':
				cities = c_name.query(c_name.musician_state == state, c_name.band_genre == genre, projection=[c_name.musician_city], distinct=True).fetch()
			else:
				cities = c_name.query(c_name.musician_state == state, projection=[c_name.musician_city], distinct=True).fetch()

			cities = sorted([x.musician_city for x in cities])
			cities.insert(0,'All')
			data = {'cities':cities}

			self.response.out.write(json.dumps(data))


class DistinctStates(views.Template):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'  
		c_name = models.musician.Musician
		if self.request.get('genre') == 'All':
			states = [x.musician_state for x in c_name.query(projection=[c_name.musician_state], distinct=True).order(c_name.musician_state).fetch()]
			states.insert(0,'All')
			self.response.out.write(json.dumps({'states':states}))

		else:
			genre = self.request.get('genre')

			states = c_name.query(c_name.band_genre == genre, projection=[c_name.musician_state], distinct=True).fetch()

			states = sorted([x.musician_state for x in states])
			states.insert(0,'All')
			data = {'states':states}

			self.response.out.write(json.dumps(data))
		

		

app = webapp2.WSGIApplication([
    ('/load-content/parameters/city.*', DistinctCities),
    ('/load-content/parameters/state.*', DistinctStates)

], debug=True)