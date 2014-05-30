from google.appengine.api import mail
import views

class Email(views.Template):

	@classmethod	
	def email(cls, subject, body, email):
		message = mail.EmailMessage(sender= "ShowTown <tom.seward@showtown.co>",
			                            subject= subject)

		message.to = email

		
		message.html = body
		
		message.send()