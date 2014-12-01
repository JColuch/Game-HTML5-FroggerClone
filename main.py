import os
import webapp2
import jinja2
import json

from google.appengine.ext import db

file_dir = os.path.join(os.path.dirname(__file__))
jinja_env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(file_dir), autoescape=True)

### Handlers ###
class MainPage(webapp2.RequestHandler):
  def get(self):
    highscores = HighScore.getTopFive()

    template = jinja_env.get_template('index.html')
    self.response.write(template.render(highscores = highscores))

  def post(self):
    #Get the parameters from the request
    initials = self.request.get('initials')
    location = self.request.get('location')
    score = int(self.request.get('score'))

    #TODO: Validate form post

    #Post to datastore
    post = HighScore.newScore(initials, location, score)
    post.put()
    self.redirect('/')



class JsonHandler(webapp2.RequestHandler):
  #SOURCE: Udacity Course: Web Dev - Lesson 5
  def get(self):
    highscores = HighScore.getTopFive()

    #Serve as JSON
    return self.render_json([s.as_dict() for s in highscores])

  #SOURCE: Udacity Course: Web Dev - Lesson 5
  def render_json(self, d):
    json_txt = json.dumps(d)
    self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    self.response.write(json_txt)



### Data Models ###
class HighScore(db.Model):
  """datastore data model for HighScore"""
  initials = db.StringProperty(required = True)
  location = db.StringProperty(required = True)
  score = db.IntegerProperty(required = True)

  @classmethod
  def newScore(cls, initials, location, score):
    """ Return new HighScore entity """
    return HighScore(initials = initials, location = location, score = score)

  @classmethod
  def getTopFive(cls):
    """ Retrieve top 5 highscores """
    q = HighScore.all()
    highscores = q.order('-score').fetch(limit=5)
    return highscores

  #SOURCE: Udacity Course: Web Dev - Lesson 5
  def as_dict(self):
    d = {'initials': self.initials,
         'location': self.location,
         'score': self.score
    }
    return d

### Utilities ###



application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/json', JsonHandler)
], debug=True)