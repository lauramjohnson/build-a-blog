#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import webapp2
import cgi
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class BlogPost(db.Model):
    subject = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    create = db.DateTimeProperty(auto_now_add = True)

class MainHandler(webapp2.RequestHandler):
    def render_front(self, subject="", blog="", error=""):
        posts = db.GqlQuery("SELECT * FROM BlogPost")

        t = jinja_env.get_template("newpost.html")
        content = t.render(subject = subject, blog=blog, error=error, posts=posts)
        self.response.write(content)

    def get(self):
        self.render_front()

    def post(self):
        subject = self.request.get("subject")
        blog = self.request.get("blog")

        if subject and blog:
            a = BlogPost(subject=subject, blog=blog)
            a.put()

            self.redirect('/')
        else:
            error = "you must have a subject and a blog post"
            self.render_front(subject, blog, error)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
