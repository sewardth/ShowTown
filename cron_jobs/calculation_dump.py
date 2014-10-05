from google.appengine.ext import ndb
import views, webapp2, models, datetime, time, logging, csv
from trend_staging import Trending

class Dump(views.Template):
    def get(self):
        overall_rank = Trending()
        overall_rank.commit_data()

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




app = webapp2.WSGIApplication([
    ('/tasks/trending/dump_data.*', Dump)

], debug=True)