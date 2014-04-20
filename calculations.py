import webapp2, json, sys, views
from google.appengine.ext import ndb
sys.path.insert(0,'libs')
import models


class LikesCount(object):


	@classmethod	
	def counts_by_musicians(cls, musician_keys):
		matches = models.voting.Voting.fetch_votes_musicians(musician_keys)
		total_matches = [x.video_one_artist_key for x in matches]+[x.video_two_artist_key for x in matches]
		win_totals = [x.voter_choice_musician_key for x in matches]
		
		
		data_dict ={}
		for x in musician_keys:
			wins = win_totals.count(x)
			totals = total_matches.count(x)
			print wins, totals
			if wins !=0 or totals != 0:
				win_percent = format((float(wins)/totals)*100,'.0f')

			else:
				win_percent = '0'
			data_dict[x]= win_percent
		return data_dict
		
		
		
			
			
			