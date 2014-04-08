

import webapp2, json, sys, views, random
sys.path.insert(0,'libs')
import models



class TrendingHandler(views.Template):
	def get(self):
		musicians_states = [{'name':'Michigan', 'abbr':'MI'}, {'name':'California', 'abbr':'CA'}, {'name':'Florida', 'abbr':'FL'}]
		template_values = {'musicians_states':musicians_states}
		self.render('trending.html', template_values)

	def post(self):
		# NOTE: we are posting genre, state and the cursor from a previous request or null if this is the initial one.
		curs = Cursor(urlsafe=self.request.get('cursor'))
		musicians, next_curs, more = models.musician.Musician.query().fetch_page(10, start_cursor=curs)
		trending_data =[]
		for x in mus_data:
			data = x.to_dict()
			del data['profile_pic'], data['latest_update'], data['user_key'], data['account_created'], data['DOB']
			data['mus_key'] = x.key.urlsafe()
			trending_data.append(data)
		if more and next_curs:
		      next = next_curs.urlsafe()
		else:
			next = None
		
		
		data = {'cursor_for_next_page':next, 'trending_data':trending_data}
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		self.response.out.write(json.dumps(data)) 


    		    		                                         		
app = webapp2.WSGIApplication([
    ('/trending', TrendingHandler)

    
], debug=True)
