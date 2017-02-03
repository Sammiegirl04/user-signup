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
#
import webapp2
import re
import cgi


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def form(self, username="", error1="", error2="", error3="", email=""):
        form = """
            <!DOCTYPE html>
            <html>
                <head>
                <title>User-signup</title>
                    <style type="text/css">
                        .error {
                            color: red;
                        }
                    </style>
                </head>
            <body>
                <h1>
                    <a href="/">User Signup</a>
                </h1>
                <br>
            <form method="post">
                <label>
                    Username:
                    <input type="text" name="username" value='""" + username + """''>
                     """ + error1 + """ <br>
                </label>
                <label>
                    Password:
                    <input type="password" name="password" value=""> """ + error2 + """
                </label><br>
                <label>
                    Verify Password:
                    <input type="password" name="verify" value="">
                </label><br>
                <label>
                    Email (optional):
                    <input type="text" name="email" value='""" + email + """'>
                    """ + error3 + """ <br>
                </label>
                <br>
                <br>
                <input type="submit" name="Submit">
            </form>
            <br>
            </body>
            </html>
            """
        return self.response.out.write(form % {"username": username,
                                                "error1": error1,
                                                "error2": error2,
                                                "error3": error3,
                                                "email": email})

    def get(self):
        username = ""
        error1 = ""
        error2 = ""
        error3 = ""
        email = ""

        self.form(username, error1, error2, error3, email)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        errors = False
        error_escaped1 = ""
        error_escaped2 = ""
        error_escaped3 = ""

        if not valid_username(username):
            error1 = "Invalid username"
            error_escaped1 = "<span class='error'>" + cgi.escape(error1) + "</span>"
            errors = True

        if not valid_password(password):
            error2 = "Invalid password"
            error_escaped2 =  "<span class='error'>" + cgi.escape(error2) + "</span>"
            errors = True

        elif not password == verify:
            error2 = "Passwords do not match"
            error_escaped2 =  "<span class='error'>" + cgi.escape(error2) + "</span>"
            errors = True

        if email == "":
            pass
        elif not valid_email(email):
            error3 = "Invalid email"
            error_escaped3 =  "<span class='error'>" + cgi.escape(error3) + "</span>"
            errors = True

        if errors:
            self.form(username, error_escaped1, error_escaped2, error_escaped3, email)
        else:
            self.redirect('/Welcome?username=' + username)



class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        content = "<h2>Welcome " + username + "!</h2>"
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Welcome', Welcome)
], debug=True)
