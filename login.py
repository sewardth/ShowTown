

class login(views.Template):
  def post(self):
    pass  #will accept users email and password for validation


app = webapp2.WSGIApplication([
    ('/login_handler', login)

], debug=True)