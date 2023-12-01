import os
import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
import time
from time import strftime
import datetime
from functools import wraps
import requests
import sqlite3
# Configure application
app = Flask(__name__)

# Connect with data base
con = sqlite3.connect("Books.db")
db = con.cursor()

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# login  -> mazen
# signup -> mazen
# logout -> mazen
# profile -> mahmoud
# home
# library 
# book -> mahmoud
# cart -> mazen
# admin 
# add book
## all books
## requests for books/updates
## requests for writers
## all users (email, state, button to change state)
## history



con.commit()
con.close()

if __name__ == '__main__':
    app.run(debug=True)