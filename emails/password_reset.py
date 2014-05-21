class reset_email():
	body = """<p>You are receiving this email because a request to reset your password was submitted on the www.showtown.co
			  website.  If you did not initiate this request, please contact <a href="mailto:info@showtown.co>info@showtown.co</a></p>

			  <p>If you did initiate this request, please click below to reset your password now.</p>"""

	closing="""<p>Sincerely,</p>
			   <p>The Showtown team</p>"""


	@classmethod
	def generate_body():
		return body

	@classmethod
	def generate_closing():
		return closing

