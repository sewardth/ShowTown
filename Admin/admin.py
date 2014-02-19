import webapp2
import models, views
from google.appengine.ext import db
import csv

class MainHandler(views.Template):
	def get(self):
		p = db.Query(models.Band).filter('approved =', '1')
		band = p.fetch(8)
		template_values = {'bands':band}
		self.render('admin.html', template_values)
		
	def post(self):
		m1_band_1 = self.request.get('m1_band_1')
		m1_band_2 = self.request.get('m1_band_2')
		m2_band_1 = self.request.get('m2_band_1')
		m2_band_2 = self.request.get('m2_band_2')
		m3_band_1 = self.request.get('m3_band_1')
		m3_band_2 = self.request.get('m3_band_2')
		m4_band_1 = self.request.get('m4_band_1')
		m4_band_2 = self.request.get('m4_band_2')
		self.band_list = [[m1_band_1, m1_band_2],
					      [m2_band_1, m2_band_2],
					      [m3_band_1, m3_band_2],
					      [m4_band_1, m4_band_2]]
		try:
			p = db.Query(models.Competition).filter('active !=', '0')
			band = p.fetch(100)	
			for x in band:
				x.active = '0'
				x.put()
				
			
		except:
			pass
			
		try:
			p = db.Query(models.LeaderBoard)
			leaders = p.fetch(100)
			db.delete(leaders)
			
		except:
			pass
			
			
		self.create_table()
		self.redirect('/admin')
		
		
	def create_table(self):
		for x in self.band_list:
			if x[0] == '':
				pass
			else:
				#video link querie
				m1 = db.Query(models.tournament).filter('band_name =', x[0])
				m1_video = m1.get()
				m2a = db.Query(models.tournament).filter('band_name =', x[1])
				m2_video = m2a.get()
				
				#photo link queries
				m1 = db.Query(models.Band).filter('band_name =', x[0])
				m1_photo = m1.get()
				m2b = db.Query(models.Band).filter('band_name =', x[1])
				m2_photo = m2b.get()
				
				d = models.Competition()
				d.band_1 = x[0]
				d.band_1_video = m1_video.band_video
				d.band_1_photo = m1_photo.band_picture
				d.band_2 = x[1]
				d.band_2_video = m2_video.band_video
				d.band_2_photo = m2_photo.band_picture
				d.put()

		
class PhotoUpdate(views.Template):
	def get(self):
		p = db.Query(models.Band).filter('approved =', '1')
		band = p.fetch(8)
		template_values = {'bands':band}
		self.render('photo.html', template_values)
		
	def post(self):
		band = self.request.get('band')
		photo = db.Blob(self.request.get('photo'))
		p = db.Query(models.Band).filter('band_name =', band)
		band = p.get()
		
		band.band_picture = photo
		band.put()
		self.redirect('/admin/update_photo')


class LeaderUpdate(views.Template):
	def post(self):
		p = db.Query(models.Competition).filter('active =', '1')
		band = p.fetch(100)
		
		for x in band:
			z = db.Query(models.Votes).filter('competition_id =', str(x.key())).filter('band_name =', x.band_1)
			band_1_votes = z.count()
			z = db.Query(models.Votes).filter('competition_id =', str(x.key())).filter('band_name =', x.band_2)
			band_2_votes = z.count()
			d = models.LeaderBoard()
			d.band_1 = x.band_1
			d.band_2 = x.band_2
			d.band_1_votes = str(band_1_votes)
			d.band_2_votes = str(band_2_votes)
			d.comp_id = str(x.key())
			d.put()



class SpreadSheet(views.Template):
	def post(self):
		p = db.Query(models.Fan)
		data = p.fetch(1000)
		self.response.headers['Content-Type'] = 'application/csv'
		c = csv.writer(self.response.out)
		c.writerow(["email","verified","created_date"])
		for x in data:
			d = []
			d.append(x.email_address)
			d.append(x.verified)
			d.append(x.createdDate)
			c.writerow(d)
		
		self.response.out.write(c)
		
		
		
class VotesData(views.Template):
	def post(self):
		p = db.Query(models.Votes)
		data = p.fetch(10000)
		self.response.headers['Content-Type'] = 'application/csv'
		c = csv.writer(self.response.out)
		c.writerow(["Comp_ID","Date","user", "Vote_For", "IP_Address"])
		for x in data:
			d = []
			d.append(x.competition_id)
			d.append(x.submission_date)
			d.append(x.user)
			d.append(x.band_name)
			d.append(x.user_ip)
			c.writerow(d)
			
		self.response.out.write(c)
			
			

app = webapp2.WSGIApplication([
    ('/admin', MainHandler),
    ('/admin/update_photo', PhotoUpdate),
    ('/admin/update_leader', LeaderUpdate),
	('/admin/spreadsheet_data', SpreadSheet),
	('/admin/votes_data', VotesData)
	

    


], debug=True)


