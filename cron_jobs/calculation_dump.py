from google.appengine.ext import ndb
import views, webapp2, models, datetime, time, logging, csv
from trend_staging import Trending

class SummaryCalcs(views.Template):
    def get(self):
        scope = self.request.get('scope')
        self.response.headers['Content-Type'] = 'application/csv'
        overall_rank = Trending()
        overall_rank.commit_data()
        
        if scope == 'Full':
            self.response.headers['Content-Disposition'] = 'attachment; filename=All_Data'+str(datetime.datetime.now())+'.csv'
            self.return_all(overall_rank)
        
        else:
            self.response.headers['Content-Disposition'] = 'attachment; filename=Summary'+str(datetime.datetime.now())+'.csv'
            self.return_summary(overall_rank)



    def return_summary(self, overall_rank):
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

    def return_all(self, overall_rank):
        """Returns all data by date for each artist"""

        c = csv.writer(self.response.out)
        c.writerow(['Musician','Date','Followers','Wins','Likes','Videos'])
        
        #loop through musician object array
        for musician in overall_rank.musicians:

            #calculate days between today and when artist opened account
            start_date = musician.account_created.date()
            today = datetime.datetime.today().date()
            delta = (today - start_date).days

            #build an array of all possible dates
            date_list = [today - datetime.timedelta(days=x) for x in range(0, delta+1)]

            #write date to rows
            for date in date_list:
                d=[]
                d.append(musician.band_name)
                d.append(date)
                d.append(musician.followers.get(date,0))
                d.append(musician.wins.get(date,0))
                d.append(musician.likes)
                d.append(musician.videos)
                c.writerow(d)
            
        self.response.out.write(c)







app = webapp2.WSGIApplication([
    ('/tasks/trending/dump_data.*', SummaryCalcs)

], debug=True)