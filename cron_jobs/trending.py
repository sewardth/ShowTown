from google.appengine.ext import ndb
import views, webapp2, models,requests, os, logging

class TrendingSelector(views.Template):
    def get(self):
    
        #kick off initial rank for all musicians
        self.cron_request('All')

        #fetch distinct states to rank
        states = models.musician.Musician.fetch_distinct_states()

        #kick off ranking for each state
        for x in states:
            self.cron_request(x.musician_state)

        self.response.out.write('job complete')
        logging.info('trending update complete')

    def cron_request(self, state):
        payload = {'selection':state}
        domain = os.environ['HTTP_HOST']
        r = requests.post("http://"+domain+"/tasks/trending/builder", data=payload)



        




app = webapp2.WSGIApplication([
    ('/tasks/trending', TrendingSelector)

], debug=True)