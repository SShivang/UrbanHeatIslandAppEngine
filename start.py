import webapp2
import logging
import re
import jinja2
import os
import time
import json

import firebase
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
		self.render("uhiportal.html")
		
class Map(MyHandler):
	def post(self):
		src = "http://maps.googleapis.com/maps/api/staticmap?size=800x600&sensor=false"
		self.render("map.html", src=src)

class Data(MyHandler):
	def get(self):
		firebas = firebase.FirebaseApplication('https://Urban-HeatIsland-Project.firebaseio.com/urban-heatisland-project.json', None)
		id = firebas.get('/id', None)
		for i in id:
			logging.info("ID"+ i)
		self.render("map.html")
		
application = webapp2.WSGIApplication([
    ('/', MainPage),
	('/map', Map),
	('/data', Data)
], debug=True)
