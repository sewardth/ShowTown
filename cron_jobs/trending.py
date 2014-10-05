from google.appengine.ext import ndb
import views, webapp2, models,requests, os, logging, time, models, csv, datetime
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

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename='+str(datetime.datetime.now())+'.csv'
        c = csv.writer(self.response.out)
        c.writerow(['Rank','Musician','Total_Points','F','W','LPV'])
        
        for x in overall_rank.musicians:
            d = []
            d.append(x.current_rank)
            d.append(x.band_name)
            d.append(x.total_points)
            d.append(x.f)
            d.append(x.w)
            d.append(x.lpv)
            c.writerow(d)
            
        self.response.out.write(c)

        end_time = time.time()

        logging.info('Trending update completed in '+ str(end_time - start_time) + ' seconds')

        




app = webapp2.WSGIApplication([
    ('/tasks/trending', TrendingSelector)

], debug=True)