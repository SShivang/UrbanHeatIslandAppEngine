import webapp2
import logging
import re
import jinja2
import os
import time

from google.appengine.ext import db

## see http://jinja.pocoo.org/docs/api/#autoescaping
def guess_autoescape(template_name):
    if template_name is None or '.' not in template_name:
        return False
    ext = template_name.rsplit('.', 1)[1]
    return ext in ('html', 'htm', 'xml')

JINJA_ENVIRONMENT = jinja2.Environment(
    autoescape=guess_autoescape,     ## see http://jinja.pocoo.org/docs/api/#autoescaping
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class MyHandler(webapp2.RequestHandler):
	def write(self, *writeArgs):    
		self.response.write(" : ".join(writeArgs))
	def render_str(self, template, **params):
		tplt = JINJA_ENVIRONMENT.get_template('templates/'+template)
		return tplt.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class MainPage(MyHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		logging.info("********** MainPage GET **********")
		python_dictionary = {}   # creating a new dictionary
		self.render("uhiportal.html", **python_dictionary)
		
class TestHandler(MyHandler):
	def post(self):


application = webapp2.WSGIApplication([
    ('/', MainPage),
	('/test', TestHandler)
], debug=True)
