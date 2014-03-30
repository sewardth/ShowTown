import views, webapp2, models, time
from helpers.form_validation import Validate as valid
from google.appengine.ext import ndb


class UnFeatureHandler(views.Template):
	def get(self):
		user = self.user_check()
		vid_key = ndb.Key(urlsafe=self.request.get('id'))
		record = vid_key.get()
		if record.acc_key == user.key:
			record.featured = False
			record.put()
			time.sleep(.5)
			self.redirect('/musician_profile')
		else:
			self.response.out.write('Not Authorized')
		
		

class FeatureHandler(views.Template):
	def get(self):
		user = self.user_check()
		vid_key = ndb.Key(urlsafe=self.request.get('id'))
		record = vid_key.get()
		
		if record.acc_key == user.key:
			videos = models.videos.Videos.query_by_account(user.key)
			for v in videos:
				if v.featured == True:
					v.featured = False
					v.put()
			
			record.featured = True
			record.put()
			time.sleep(.5)
			self.redirect('/musician_profile')
		else:
			self.response.out.write('Not Authorized')
		
		
		
	
class RemoveHandler(views.Template):
	def get(self):
		user = self.user_check()
		vid_key = ndb.Key(urlsafe=self.request.get('id'))
		record = vid_key.get()
	
		if record.acc_key == user.key:
			vid_key.delete()
			time.sleep(.5)
			self.redirect('/musician_profile')
		else:
			self.response.out.write('Not Authorized')
	
class AddHandler(views.Template):
	def post(self):
		submission_video = valid.get_video(self.request.get('video_url'))
		acc_key = self.user_check()
		musician = models.musician.Musician.query_by_account(acc_key.key)
		video = models.videos.Videos(embed_link = submission_video['embed_link'],
									acc_key = acc_key.key,
									musician_key = musician.key,
									musician_name = musician.band_name,
									genre_tag = None,
									video_title = submission_video['title'],
									featured = False).put()
		time.sleep(.5)
		self.redirect('/musician_profile')

	
app = webapp2.WSGIApplication([
   
    ('/video_unfeature*', UnFeatureHandler),
	('/video_feature', FeatureHandler),
    ('/video_remove*', RemoveHandler),
    ('/video_add*', AddHandler)


], debug=True)