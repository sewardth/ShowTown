import views, webapp2, models, time, json, stats_updater as stats
from google.appengine.ext import ndb



class VoteHandler(views.Template):
	def get(self):
		user = self.user_check()
		video_one = ndb.Key(urlsafe = self.request.get('left_vid'))
		video_one_artist_key = ndb.Key(urlsafe = self.request.get('left_mus_id'))
		video_two = ndb.Key(urlsafe = self.request.get('right_vid'))
		video_two_artist_key = ndb.Key(urlsafe = self.request.get('right_mus_id'))
		if self.request.get('win') == '':
			mus_choice = None
			voter_choice = None
		else:
			voter_choice =  ndb.Key(urlsafe = self.request.get('win'))
			if voter_choice == video_one:
				mus_choice = video_one_artist_key
			else:
				mus_choice = video_two_artist_key
				
		vote = models.voting.Voting.get_by_vote(user.key, [video_one, video_two])
		if vote == None:
			vote = models.voting.Voting(voter_acc_key = user.key,
										voter_type = user.account_type,
										video_one = video_one,
										video_one_artist_key = video_one_artist_key,
										video_two = video_two,
										video_two_artist_key = video_two_artist_key,
										voter_choice = voter_choice,
										voter_choice_musician_key = mus_choice,
										video_set_check = [video_one, video_two],
										voter_ip = self.request.remote_addr).put()
	
			time.sleep(.5)

			#Update musician and video model counts
			stats.MusicianStats.update_wins(video_one_artist_key)
			stats.MusicianStats.update_wins(video_two_artist_key)
			stats.MusicianStats.update_total_matches(video_one_artist_key)
			stats.MusicianStats.update_total_matches(video_two_artist_key)

			stats.VideoStats.update_wins(video_one)
			stats.VideoStats.update_wins(video_two)
			stats.VideoStats.update_total_matches(video_one)
			stats.VideoStats.update_total_matches(video_two)



			self.redirect('/')
		else:
			self.response.out.write('Record Already Exists')



class LikeHandler(views.Template):
	def post(self):
		user = self.user_check()
		musician_key = ndb.Key(urlsafe = self.request.get('mus_id'))
		video_key = ndb.Key(urlsafe = self.request.get('vid_id'))
		if self.existing(user.key, video_key):
			pass
		else:
			data = models.likes.Likes(user_key = user.key,
								  musician_key = musician_key,
								  video_key = video_key).put()

			time.sleep(.2)

			#update musician and video model counts for likes
			musician_likes = stats.MusicianStats.update_likes(musician_key)
			musician_wins = stats.MusicianStats.update_wins(musician_key)
			video_likes = stats.VideoStats.update_likes(video_key)
			video_wins = stats.VideoStats.update_wins(video_key)

			time.sleep(.5)

			self.response.out.write(json.dumps({'musician_likes':musician_likes,
												'musician_wins': musician_wins,
												'video_likes':video_likes, 
												'video_key':video_key.urlsafe(),
												'video_wins':video_wins}))


	def existing(self, user_key, video_key):
		test = models.likes.Likes.get_existing(user_key, video_key)
		return test


app = webapp2.WSGIApplication([
   
    ('/vote/likes.*', LikeHandler),
    ('/vote.*', VoteHandler)


], debug=True)