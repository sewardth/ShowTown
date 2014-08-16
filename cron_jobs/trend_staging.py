from google.appengine.ext import ndb
import views, webapp2, models, datetime, time, logging

class Trending(views.Template):
    """Builds current trending ranks and inserts records into trending model"""
    def post(self):
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

        selection = self.request.get('selection')
        musicians = mus.query()

        #filter by state if selection
        if selection != 'All': musicians = musicians.filter(mus.musician_state == selection)

        #pull musicians
        musicians = musicians.fetch()

        #fetch follower transactions
        fol = models.following.Following
        follower_trans = fol.query().fetch()

        #videos posted
        self.videos = [x.musician_key for x in models.videos.Videos.query().fetch()]

        #fetch head-to-head wins
        wins = models.voting.Voting
        votes = wins.query().fetch()

        #fetch likes per video
        vids = models.likes.Likes
        video_likes = vids.query().fetch()

        #build calculation dictionaries
        self.recent_calcs(follower_trans, votes, video_likes)
        self.wins_theta = self.theta_builder(votes,'voter_choice_musician_key','vote_time')
        self.follower_theta = self.theta_builder(follower_trans,'followed_entity_key', 'followed_date')


        #build ranks
        musicians = self.rank_builder(musicians)

        #set ranks
        self.set_ranks(musicians, selection)

        end_time = time.clock() - start_time
        logging.info(str(end_time) + " seconds - " + selection) #logs process time
        self.response.out.write('Finished in ' + str(end_time) + ' seconds')

    def set_ranks(self,musicians, selection):
        #sort by rank
        ranks = sorted(musicians, key = lambda x: x.total_points, reverse = True)

        if selection == 'All':
            for i, obj in enumerate(ranks):
                obj.current_rank = i+1

        else:
            for i, obj in enumerate(ranks):
                obj.state_rank = i+1

        ndb.put_multi(ranks)

    
    def rank_builder(self, musicians):
        for x in musicians:
            following_stats = self.following.get(x.key,{})
            #like_stats = self.likes.get(x.key,{})
            win_stats = self.wins.get(x.key,{})
            followers_theta = self.theta_series(x.key, x.account_created, self.follower_theta)
            wins_theta = self.theta_series(x.key, x.account_created, self.wins_theta)


            #followers calc
            f = following_stats.get('today',0) + (following_stats.get('change',0)*followers_theta)+(x.musician_stats.get('followers',0)*followers_theta)

            #wins calc
            w = win_stats.get('today',0) + (win_stats.get('change',0)*wins_theta)+(x.musician_stats.get('head_to_head_wins',0)*wins_theta)

            #likes calculation
            vids_posted = self.videos.count(x.key)
            if x.musician_stats.get('likes',0) == 0 or vids_posted == 0:
                lpv = 0
            else:
                lpv = x.musician_stats.get('likes')/float(vids_posted)

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


    def theta_builder(self, query, key_name, date_name):
        """Builds a dictionary of key:{date:count} for a query"""
        data ={}
        for x in query:
            lookup = data.get(getattr(x,key_name),None)
            if lookup:
                count = lookup.get(getattr(x,date_name).date(),0)
                if count == 0:
                    data[getattr(x,key_name)][getattr(x,date_name).date()] = 1
                else:
                    data[getattr(x,key_name)][getattr(x,date_name).date()] = count+1

            else:
                #set artist key in dict
                data[getattr(x,key_name)] = {}

                #set initial date with count 1
                data[getattr(x,key_name)][getattr(x,date_name).date()] = 1

        return data


    def theta_series(self, key, account_created_date, dictionary):
        """returns a series of 1/days * count for each record"""
        data = dictionary.get(key, None)
        series =[]
        if data:
            for x in data:
                days = (x - account_created_date.date()).days
                calc = (1.0/(days+1))*data[x]
                series.append(calc)
        else:
            series =[0]
        return sum(series)



app = webapp2.WSGIApplication([
    ('/tasks/trending/builder.*', Trending)

], debug=True)