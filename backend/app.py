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

# inportant functions --------------------------------------------------------------------
def getData(db_fetch, db_disc):
    cols_disc = [col[0] for col in db_disc]
    rows = [dict(zip(cols_disc,row)) for row in db_fetch]
    return rows

def getQuaryFromDataBase(database = "Books.db" ,quary_text = "", *args):
    # make a connect with the database
    con = sqlite3.connect(database)
    # create cursor with called db
    db = con.cursor()
    con.row_factory = sqlite3.Row
    # try to get the data 
    try:
        db.execute(quary_text,tuple(args))
        data = getData(db.fetchall(), db.description)
        con.commit()
        db.close()
        con.close()
    except:
        return None
    return data

def createErrorMessage(err_state = False, err_type = none, err_mesg_txt = none):
    error_message = {"error_state" : err_state,
                    "error_type" : err_type,
                    "error_message_text" : err_mesg_txt
                    }
    return error_message
# ----------------------------------------------------------------------------------------

# login  -> mazen
# signup -> mazen
# logout -> mazen
# profile -> mahmoud
@app.route("/profile",  methods=["GET", "POST"])
@login_required
def profile():
    # change password
    if request.method == "POST":
        pass

    # show profile
    else:
        personInfo = getQuaryFromDataBase("Books.db",
                                          "select * from user where user_id = ?",
                                          int(session["user_id"]),
                                          )
        return render_template("try.html")


# home
# library 
# book -> mahmoud
@app.route("/book/<int:bookId>",  methods=["GET", "POST"])
@login_required
def book(bookId):
    # get data from  database with the quary below
    bookInfo = getQuaryFromDataBase("Books.db",
                                    "select * from Book where book_id = ?",
                                    bookId,
                                    )
    # if user wants to add an item to thier cart
    if request.method == "POST":
        # handling 
        if session.get("user_id") == None:
            error_message = createErrorMessage(True,
                                                "login_required",
                                                "You have to login fisrt to be able to buy this item.")

        # handling the quantity error when quantity be non positive value
        if request.form.get("quantity") < 1:
            # create the error message as object 
            error_message = {"error_state" : True,
                            "error_type":"invaled value",
                            "error_message_text" : "Quantity can not be non positive!"}
            # return the page with the ma=essage
            # do not forget to add the bookInfo to the page. 
            return render_template("try.html", 
                                   page_name = "error message : quantity can not be non positive!", 
                                   err_mes = error_message)

        # check if these is any item in the cart before (cart has been created)
        quantityOfBook = 0 # TODO need to pass as arg!
        if "cart" in session: # if cart already created
            if session["cart"].get(bookId):
                session["cart"][bookId] = int(request.form.get("quantity"))
            else:
                session["cart"][bookId] = int(request.form.get("quantity"))
        else: # if cart not created
            session["cart"] = {} # cart will be a dict
            session["cart"][bookId] = int(request.form.get("quantity"))
        if "cart" in session:
            quantityOfBook = int(request.form.get("quantity")) # TODO need to pass as arg!
        return render_template("try.html", page_name = f"add to cart book id = {bookId}")
    
    # if the user request the page via get method
    else:
        error_message = {"error_state" : False,
                        "error_type":"none",
                        "error_message_text" : "none"}
        if bookInfo != None and len(bookInfo) > 0:
            title = bookInfo[0]["title"]
        else:
            title = None
            error_message["error_state"] = True
            error_message["error_type"] = "not found"
            error_message["error_message_text"] = "This book is not found at current time!"
        return render_template("try.html",
                                title = title,
                                page_name = f"bookId = {bookId}",
                                err_mes = error_message)
# cart -> mazen
# admin 
# add book
## all books
## requests for books/updates
## requests for writers
## all users (email, state, button to change state)
## history




if __name__ == '__main__':
    app.run(debug=True)