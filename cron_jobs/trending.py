from google.appengine.ext import ndb
import views, webapp2, models,requests

class TrendingSelector(views.Template):
    def get(self):
    
        #kick off initial rank for all musicians
        self.cron_request('All')

        #fetch distinct states to rank
        states = models.musician.Musician.fetch_distinct_states()

        #kick off ranking for each state
        for x in states:
            self.cron_request(x.musician_state)



    def cron_request(self, state):
        payload = {'selection':state}
        r = requests.post("http://localhost:9080/tasks/trending/builder", data=payload)
        return 1



        




app = webapp2.WSGIApplication([
    ('/tasks/trending', TrendingSelector)

], debug=True)