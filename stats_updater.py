from google.appengine.ext import ndb
import models, json


class MusicianStats:

	@classmethod
	def update_wins(cls, musician_key):
		wins = models.voting.Voting.return_win_count(musician_key)
		musician = musician_key.get()
		musician.musician_stats['head_to_head_wins']=wins
		musician.put()


	@classmethod
	def update_total_matches(cls, musician_key):
		total_matches = models.voting.Voting.return_matches_count(musician_key)
		musician = musician_key.get()
		musician.musician_stats['total_matchups']=total_matches
		musician.put()


	@classmethod
	def update_likes(cls, musician_key):
		likes = models.likes.Likes.count_by_musician(musician_key)
		musician = musician_key.get()
		musician.musician_stats['likes']=likes
		musician.put()


	@classmethod
	def update_followers(cls, musician_key):
		followers = models.following.Following.return_follower_count(musician_key)
		musician = musician_key.get()
		musician.musician_stats['followers']=followers
		musician.put()



class VideoStats:

	@classmethod
	def update_wins(cls, video_key):
		wins = models.voting.Voting.return_win_count_videos(video_key)
		video = video_key.get()
		video.video_stats['head_to_head_wins']=wins
		video.put()


	@classmethod
	def update_total_matches(cls, video_key):
		total_matches = models.voting.Voting.return_matches_count_videos(video_key)
		video = video_key.get()
		video.video_stats['total_matchups']=total_matches
		video.put()


	@classmethod
	def update_likes(cls, video_key):
		likes = models.likes.Likes.count_by_video(video_key)
		video = video_key.get()
		video.video_stats['likes']=likes
		video.put()