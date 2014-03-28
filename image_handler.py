import views, webapp2, models, time
from google.appengine.api import images
from google.appengine.ext import ndb


class ImageHandler(views.Template):
	def get(self):
		key = ndb.Key(urlsafe = self.request.get('id'))
		width self.request.get('width')
		height = self.request.get('height')
		pic = key.get()
		if pic.profile_pic:
			image = images.Image(image_data = pic.band_2_photo)
			desired_wh_ratio = float(width) / float(height)
			wh_ratio = float(image.width) / float(image.height)
			image.resize(width=width, height = height)
			img = image.execute_transforms(output_encoding=images.JPEG)
			self.response.headers['Content-Type'] = 'image/jpeg'
			self.response.out.write(img)
		else:
			self.response.out.write('No image')
		
		
		
		
app = webapp2.WSGIApplication([
   
    ('/imgs*', ImageHandler),



], debug=True)