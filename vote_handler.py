import views, webapp2, models, time
from google.appengine.ext import ndb


class VoteHandler(views.Template):
	def get(self):
		user = self.user_check()
		video_one = ndb.Key(urlsafe = self.request.get('left_vid'))
		video_one_artist_key = ndb.Key(urlsafe = self.request.get('left_mus_id'))
		video_two = ndb.Key(urlsafe = self.request.get('right_vid'))
		video_two_artist_key = ndb.Key(urlsafe = self.request.get('right_mus_id'))
		if self.request.get('win') == '':
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
			self.redirect('/')
		else:
			self.response.out.write('Record Already Exists')
	
app = webapp2.WSGIApplication([
   
    ('/vote*', VoteHandler)


], debug=True)