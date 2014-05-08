from google.appengine.ext import ndb
import views, webapp2, models, datetime

class Trending(views.Template):
    """Builds current trending ranks and inserts records into trending model"""
    def get(self):
        musicians_query = models.musician.Musician.fetch_all()
        self.likes = self.fetch_likes()
        self.votes = self.fetch_votes()
        self.wins = self.fetch_wins()
        self.following = self.fetch_following()
        self.videos = self.fetch_videos()

        #build models
        self.build_calcs(musicians_query)



    def fetch_likes(self):
        query = models.likes.Likes.recent_trends()
        return [x.musician_key for x in query]

    def fetch_votes(self):
        self.matches = models.voting.Voting.recent_trends()
        return [x.video_one_artist_key for x in self.matches]+[x.video_two_artist_key for x in self.matches]

    def fetch_wins(self):
        return [x.voter_choice_musician_key for x in self.matches]

    def win_percent(self, musicians):
        return [float(self.wins.count(x))/self.votes.count(x) for x in musicians]

    def fetch_following(self):
        query = models.following.Following.recent_trends()
        return [x.followed_entity_key for x in query]

    def fetch_videos(self):
        query = models.videos.Videos.fetch_all()
        return [x.musician_key for x in query]

    def build_calcs(self, musicians):
        #convert musicians to key list
        musician_list = [x.key for x in musicians]
        win_percents = self.win_percent(musician_list)

        likes_rank = self.rank_by_value(musician_list, self.likes)
        following_rank = self.rank_by_value(musician_list, self.following)
        win_percent_rank = self.rank_by_value(musician_list, win_percents, count = False)

        #insert into NDB class Trending
        for x in musician_list:
            obj = models.trending.Trending(musician_key = x,
                                          likes_rank = likes_rank[x],
                                          following_rank = following_rank[x],
                                          win_rank = win_percent_rank[x]).put()


    def rank_by_value(self, key_list, value_list, count = True):
        #calculate like count by musician
        if count: #Counts number of occurence of x in key list that are in value list.  Optional because win percent is already calculated
            counter = [value_list.count(x) for x in key_list]
        else:
            counter = value_list
        mapping =  dict(zip(key_list, counter))
        return {x:sorted(counter, reverse =True).index(mapping[x])+1 for x in mapping}



app = webapp2.WSGIApplication([
    ('/tasks/trending', Trending)

], debug=True)