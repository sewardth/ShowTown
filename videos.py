import views, webapp2, models, time
from helpers.form_validation import Validate
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
	pass

		
		
app = webapp2.WSGIApplication([
   
    ('/video_unfeature*', UnFeatureHandler),
	('/video_feature', FeatureHandler),
    ('/video_remove*', RemoveHandler),
    ('/video_add*', AddHandler)


], debug=True)