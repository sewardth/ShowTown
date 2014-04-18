import webapp2, json, sys, views
from google.appengine.ext import ndb
sys.path.insert(0,'libs')
import models


class MatchupLikes(object):
	def __init__(self, musician_keys = None, video_keys = None, user_key = None):
		#data for like counts
		self.total_votes = models.voting.Voting.fetch_votes_musicians(musician_keys)
		self.total_matches = [x.video_one_artist_key for x in self.total_votes]
		self.likes = [x.voter_choice_musician_key for x in self.total_votes]
		
		#data for followed
		self.user_followed = models.following.Following.fetch_by_user(user_key)
		self.followed = [x.followed_entity_key for x in self.user_followed]
		
		
	def count_likes(self, musician_list, key_label):
	for x in musician_list:
		data = x.to_dict()
		artist_total_matches = self.total_matches.count(data['key_label'])
		data['artist_likes'] = self.likes.count(data['key_label'])
		
		if artist_likes !=0 or artist_total_matches !=0:
			data['win_percent'] = format((float(artist_likes)/artist_total_matches)*100, '.0f')
		else: 
			data['win_percent'] = '0'
	return data
		
		
		#if x.key_label in followed: x.one_followed = True