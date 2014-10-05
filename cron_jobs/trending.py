from google.appengine.ext import ndb
import views, webapp2, models,requests, os, logging, time, models
from trend_staging import Trending

class TrendingSelector(views.Template):
    def get(self):
        start_time = time.time()
        overall_rank = Trending()
        overall_rank.commit_data()

        states = [x.musician_state for x in models.musician.Musician.fetch_distinct_states()]
        for state in states:
            obj = Trending(state)
            obj.commit_data()

        end_time = time.time()
        self.response.out.write('Trending update completed in '+ str(end_time - start_time) + ' seconds')


        logging.info('Trending update completed in '+ str(end_time - start_time) + ' seconds')

        




app = webapp2.WSGIApplication([
    ('/tasks/trending', TrendingSelector)

], debug=True)