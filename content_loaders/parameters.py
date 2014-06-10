import webapp2, sys, views, json, logging, models
sys.path.insert(0,'libs')


class DistinctCities(views.Template):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'  
		if self.request.get('state') == 'All':
			self.response.out.write(json.dumps({'cities':['All']}))

		else:
			state = self.request.get('state')

			cities = models.musician.Musician.fetch_distinct_cities(state)
			cities = [x.musician_city for x in cities]+['All']
			data = {'cities':sorted(cities)}

			self.response.out.write(json.dumps(data))
		

		

app = webapp2.WSGIApplication([
    ('/load-content/parameters/city.*', DistinctCities)
], debug=True)