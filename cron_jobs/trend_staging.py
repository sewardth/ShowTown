from google.appengine.ext import ndb
import views, webapp2, models, datetime, time, logging

class Trending(views.Template):
    """Builds current trending ranks and inserts records into trending model"""
    follower_coef = .25
    wins_coef = .35
    likes_coef = .1

    def __init__(self, state_param = 'All'):

        #Determine weather to grab all musicians or filter by state. 
        if state_param == 'All':
            self.musicians = models.musician.Musician.fetch_all()
        else:
            self.musicians = models.musician.Musician.filter_by_state(state_param)

        #Create key array for filtering
        musician_keys = [x.key for x in self.musicians]

        #Query videos, likes, and matchups
        self.videos = [x.musician_key for x in models.videos.Videos.filter_by_state(musician_keys)]
        self.matchups = models.voting.Voting.fetch_votes_musicians(musician_keys)
        self.likes = [x.musician_key for x in models.likes.Likes.fetch_for_musicians(musician_keys)]
        self.followers = models.following.Following.fetch_followers_count(musician_keys)


        #build dictionary mappings
        follower_map = self.__map_objects_to_dates(self.followers,'followed_entity_key', 'followed_date')
        wins_map = self.__map_objects_to_dates(self.matchups,'voter_choice_musician_key','vote_time')

        #calculate series for each list
        self.follower_calcs = self.__calculate_series(follower_map)
        self.wins_calcs = self.__calculate_series(wins_map)

        #build total points property on musicians object
        self.__build_ranks()

        #update database
        self.__rank_musicians(state_param)


        
 
    def __map_objects_to_dates(self, object_list, key_property, date_property):
        #takes a list of objects and returns a dictionary of {key:date{count}}
        object_mapping={}
        for x in object_list:
            key = getattr(x,key_property)
            date = getattr(x,date_property).date()
            
            key_check = object_mapping.get(key, False)

            if key_check:
                count = object_mapping[key].get(date,0)
                object_mapping[key][date] = count+1
            else:
                object_mapping[key] = {date:1}

        return object_mapping


    def __calculate_series(self, map_list):
        #takes a mapping and calculates daily changes / theta
        today = datetime.datetime.now().date()

        #create blank dictionary to store {key:points}
        calculation_mapping ={}

        #loop through list of keys in map_list
        for key in map_list:
            series_percent_change=[]
            series_count = []
            count_today = map_list[key].get(today,0)

            #loop through dates in each key in map_list
            for date in map_list[key]:
                theta = 1.0/(today-date).days

                #build series_count array with theta * values
                series_count.append(theta*map_list[key][date])

                #calculate daily percent change with midpoint formula
                day_count = map_list[key][date]
                prev_day_date = date - datetime.timedelta(days = -1)
                prev_day_count = map_list[key].get(prev_day_date,0)

                #build series percent change
                try:
                    calc = theta* ((day_count - float(prev_day_count))/((day_count + float(prev_day_count))/2))
                
                except ZeroDivisionError:
                    calc = 0
                    
                series_percent_change.append(calc)


            calculation_mapping[key] = count_today + sum(series_percent_change) + sum(series_count)

        return calculation_mapping


    def __build_ranks(self):
        for x in self.musicians:
            try:
                lpv = float(self.likes.count(x.key))/ self.videos.count(x.key)

            except ZeroDivisionError:
                lpv = 0.0

            setattr(x,'total_points',(Trending.follower_coef * self.follower_calcs.get(x.key,0))+(Trending.wins_coef * self.wins_calcs.get(x.key,0)) + (Trending.likes_coef * lpv))
            setattr(x,'lpv',lpv)
            setattr(x,'f',self.follower_calcs.get(x.key,0))
            setattr(x,'w',self.wins_calcs.get(x.key,0))

        self.musicians = sorted(self.musicians, key = lambda x: x.total_points, reverse = True)


    def __rank_musicians(self, scope):
        if scope == 'All':
            prop = 'current_rank'
        else:
            prop = 'state_rank'

        for index, musician in enumerate(self.musicians):
            setattr(musician,prop,index+1)

        

    def commit_data(self):
        ndb.put_multi(self.musicians)

    















app = webapp2.WSGIApplication([
    ('/tasks/trending/builder.*', Trending)

], debug=True)