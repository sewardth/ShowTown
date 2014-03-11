import datetime


class Cookie(object):
	
	@staticmethod
	def set_cookie(cookie, response):
		response.headers.add_header('Set-Cookie', cookie)
	
	@staticmethod	
	def create_cookie(cookie_name, cookie_value):
		expires = datetime.datetime.now() + datetime.timedelta(days=14)
		date = expires.strftime('%a, %d %b %Y %H:%M:%S')
		cookie = ' %s=%s, expires=%s, path=/, domain=.showtown.co;' %(cookie_name, cookie_value, date)
		return cookie
		
	@staticmethod
	def _grab_cookies(request):
		user_id = request.cookies.get('_auth_')
		session_id = request.cookies.get('_term_')
		return {'user':user_id, 'session' :session_id}