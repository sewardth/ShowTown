from google.appengine.ext import ndb
import views, webapp2, models, datetime, time, logging, csv

class Trending(views.Template):
    """Builds current trending ranks and inserts records into trending model"""
    def get(self):
        start_time = time.clock() #used to calculate process time for monitoring

        #set coefficients 
        self.follow_coef = .35
        self.wins_coef = .5
        self.likes_coef = .15

        #get current date and date -1
        today = datetime.datetime.now()
        yesterday = datetime.datetime.now() - datetime.timedelta(hours=24)
        self.today = today.date()
        self.yesterday = yesterday.date()

        #set base class for musician models
        mus = models.musician.Musician

        selection = 'All'
        musicians = mus.query()

        #filter by state if selection
        if selection != 'All': musicians = musicians.filter(mus.musician_state == selection)

        #pull musicians
        musicians = musicians.fetch()

        #fetch follower transactions
        fol = models.following.Following
        follower_trans = fol.query(fol.followed_date>= yesterday).fetch()

        #videos posted
        self.videos = [x.musician_key for x in models.videos.Videos.query().fetch()]

        #fetch head-to-head wins
        wins = models.voting.Voting
        votes = wins.query(wins.vote_time >= yesterday).fetch()

        #fetch likes per video
        vids = models.likes.Likes
        video_likes = vids.query(vids.like_time>= yesterday).fetch()

        #build calculation dictionaries
        self.recent_calcs(follower_trans, votes, video_likes)

        #build ranks
        musicians = self.rank_builder(musicians)

        #set ranks
        ranks = self.set_ranks(musicians, selection)

        #dump to CSV
        self.csv_dump(ranks)

        end_time = time.clock() - start_time
        logging.info(str(end_time) + " seconds - " + selection) #logs process time
        self.response.out.write('Finished in ' + str(end_time) + ' seconds')


    def csv_dump(self, ranks):
        ranks = sorted(ranks, key = lambda x: x.current_rank)
        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename={time}.csv'.format(time=datetime.datetime.now())
        c = csv.writer(self.response.out)
        c.writerow(["Rank","Musician","Total Points", "F", "W","LPV"])
        for x in ranks:
            d = []
            d.append(int(x.current_rank))
            d.append(x.band_name)
            d.append(int(x.total_points))
            d.append(int(x.f))
            d.append(int(x.w))
            d.append(int(x.lpv))
            c.writerow(d)
            
        self.response.out.write(c)

    def set_ranks(self,musicians, selection):
        #sort by rank
        ranks = sorted(musicians, key = lambda x: x.total_points, reverse = True)

        if selection == 'All':
            for i, obj in enumerate(ranks):
                obj.current_rank = i+1

        else:
            for i, obj in enumerate(ranks):
                obj.state_rank = i+1

        return ranks

    
    def rank_builder(self, musicians):
        for x in musicians:
            following_stats = self.following.get(x.key,{})
            #like_stats = self.likes.get(x.key,{})
            win_stats = self.wins.get(x.key,{})
            theta = (self.today - x.account_created.date()).days

            #followers calc
            f = following_stats.get('today',0) + (following_stats.get('change',0)*theta)+(x.musician_stats.get('followers',0)*theta)
            setattr(x,'f',f)

            #wins calc
            w = win_stats.get('today',0) + (win_stats.get('change',0)*theta)+(x.musician_stats.get('head_to_head_wins',0)*theta)
            setattr(x,'w',w)

            #likes calculation
            vids_posted = self.videos.count(x.key)
            if x.musician_stats.get('likes',0) == 0 or vids_posted == 0:
                lpv = 0
            else:
                lpv = x.musician_stats.get('likes')/float(vids_posted)
            setattr(x,'lpv',lpv)

            setattr(x,'total_points',(self.follow_coef * f) + (self.wins_coef*w) + (self.likes_coef*lpv))

        return musicians





    def recent_calcs(self, follower_trans, votes, video_likes):
        #builds day and day -1 dictionaries
        self.following = self.percent_mapping(follower_trans, 'followed_date', 'followed_entity_key')
        self.wins = self.percent_mapping(votes, 'vote_time', 'voter_choice_musician_key')
        #self.likes = self.percent_mapping(video_likes, 'like_time', 'musician_key')

    
    def percent_mapping(self, query, date_name, key_name):

        #create arrays with muscians keys for day and day-1
        todays_count = [getattr(x,key_name) for x in query if datetime.datetime.date(getattr(x,date_name)) == self.today]
        yesterday_count = [getattr(x,key_name) for x in query if datetime.datetime.date(getattr(x,date_name)) == self.yesterday]

        #map data using dictionary and return
        data = {}
        for x in query:
            today = todays_count.count(getattr(x,key_name))
            yesterday = yesterday_count.count(getattr(x,key_name))
            if today > yesterday and yesterday != 0:
                change = (today-yesterday)/float(yesterday)
            elif today > yesterday and yesterday == 0:
                change = 1.0
            else:
                change = 0.0

            data[getattr(x,key_name)] = {'change':change, 'today':today,'yesterday':yesterday}

        return data






app = webapp2.WSGIApplication([
    ('/tasks/trending/dump_data.*', Trending)

], debug=True)