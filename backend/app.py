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

# login  -> mazen
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        """Ensure username was submitted"""
        email = request.form.get("email")
        password = request.form.get("password")
        # Ensure email was submitted
        if not email:
            return render_template("login.html", error_message="message", invalid=True)
        # Ensure password was submitted
        elif not password:
            return render_template("login.html", error_message="message", invalid=True)
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # Query database for username
        db.execute("SELECT * FROM users WHERE email = ?", (email,))
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        rows = [dict(zip(columns, row)) for row in db.fetchall()]

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return render_template("login.html", error_message="message", invalid=True)
        
        if rows[0]["password"] != password:
            return render_template("login.html", error_message="message", invalid=True)
        
        # commit and close database
        con.commit()
        db.close()
        con.close()
        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", error_message="", invalid=False)

# signup -> mazen
@app.route("/signup", methods=["GET", "POST"])
def signup():
    session.clear()
    if request.method == "POST":
        # retrive username from register form
        email = request.form.get("email")

        # retrive fullname from register form
        fullname = request.form.get("fullname")

        # retrive password from register form
        password = request.form.get("password")

        # retrive confirm from register form
        confirm = request.form.get("confirm")

        # check if user provide valid username
        if not email:
            # wail for render the register page with error message
            return render_template("signup.html", error_message="message", invalid=True)

        # check if user provide valid password
        if not password:
            return render_template("signup.html", error_message="message", invalid=True)

        # check if user provide valid confirm
        if not confirm:
            return render_template("signup.html", error_message="message", invalid=True)

        # check if password equals the confirmation password
        if password != confirm:
            return render_template("invalid.html", error_message="message", invalid=True)

        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # retrive all users from database with the same email
        db.execute("SELECT * FROM User WHERE email = ?;", (email,))

        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        users = [dict(zip(columns, row)) for row in db.fetchall()]

        # check if username registered before
        if len(users) >= 1:
            return render_template("signup.html", error_message="message", invalid=True)

        # after validating all conditions insert new user into database
        db.execute("INSERT INTO User(email,full_name,password) VALUES(?,?,?);", (email, fullname, password,))

        # retrive new user id from database
        db.execute("SELECT * FROM users WHERE username=?", (email,))

        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        registrant = [dict(zip(columns, row)) for row in db.fetchall()]

        # add user id to session
        session["user_id"] = registrant[0]["id"]

        # commit changes
        con.commit()
        db.close()
        con.close()

        # redirect to the main page
        return redirect("/")
    else:
        return render_template("signup.html", error_message="", invalid=False)

# logout -> mazen
@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

# profile -> mahmoud
# home
# library 
# book -> mahmoud
# cart -> mazen
                # session["cart"] = []
@app.route("/cart/add/<book_id>", methods=["GET", "POST"])
@login_required
def add_to_cart(book_id):
    """Add book to cart"""
    if request.method == "GET":
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # retrive all books from database with the same book_id
        db.execute("SELECT * FROM Book WHERE book_id = ? WHERE state = ?;", (book_id,1,))

        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        books = [dict(zip(columns, row)) for row in db.fetchall()]

        # add book to cart
        session["cart"].append(books[0])

        # commit changes
        con.commit()
        db.close()
        con.close()

        # redirect to the main page
        return redirect("/")
    else:
        # I don't know what to do here
        return "TODO"

@app.route("/cart/remove/<book_id>", methods=["GET", "POST"])
@login_required
def remove_from_cart(book_id):
    """Remove book from cart"""
    if request.method == "GET":
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # retrive all books from database with the same book_id
        db.execute("SELECT * FROM Book WHERE book_id = ? WHERE state = ?;", (book_id,1,))

        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        books = [dict(zip(columns, row)) for row in db.fetchall()]

        # remove book from cart
        session["cart"].remove(books[0])

        # commit changes
        con.commit()
        db.close()
        con.close()

        # redirect to the main page
        return redirect("/")
    else:
        # I don't know what to do here
        return "TODO"

@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    """Show cart"""
    if request.method == "GET":
        return render_template("cart.html", cart=session["cart"])
    else:
        # retrive data from form
        address = request.form.get("address")
        phone = request.form.get("phone")
        user_id = session["user_id"]
        date_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        total = 0
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # each book in session["cart"] has [book_id, title, image, price, quantity, writer_id, category_id]
        # ! I think about error why
        # ! while i'm updating the book['quantity'] in session["cart"] if i found an error 
        # ! and i returned the user if he want to change the quantity of the book
        # ! when compare we will compare with the updated quantity(from prevous request) not the original quantity(in database)
        for book in session["cart"]:
            # quantity_name = quantity_[book_id] this name will be the same as the name of the input in cart.html form
            quentity_name = "quentity_" + str(book["book_id"])
            # retrive new quantity from form
            new_quantity = request.form.get(quentity_name)
            # check if new quantity is valid
            try:
                new_quantity = int(new_quantity)
            except ValueError:
                return render_template("cart.html", cart=session["cart"], error_message="message", invalid=True)
            # check if new quantity is valid
            if new_quantity < 0:
                return render_template("cart.html", cart=session["cart"], error_message="message", invalid=True)
            # check if new quantity is valid
            if new_quantity > book["quantity"]:
                return render_template("cart.html", cart=session["cart"], error_message="message", invalid=True)
            # update quantity in session["cart"]
            book["quantity"] = new_quantity
            # update quantity in database
            total += book["price"] * book["quantity"]
        
        # check if total is valid with user balance
        """TODO"""

        # insert into bill table first
        db.execute("INSERT INTO Bill(address, phone, user_id, date_time, total) VALUES(?,?,?,?);", (address, phone, user_id, date_time, total,))
        # retrive bill id from database
        db.execute("SELECT * FROM Bill WHERE user_id=? AND date_time=?;", (user_id, date_time,))
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        bills = [dict(zip(columns, row)) for row in db.fetchall()]
        bill_id = bills[0]["bill_id"]
        # insert into order table they have same bill
        for book in session["cart"]:
            db.execute("INSERT INTO Order(bill_id, book_id, quantity, price_per_book) VALUES(?,?,?,?);", (bill_id, book["book_id"], book["quantity"], book["price"],))
        # update quantity in database
        for book in session["cart"]:
            db.execute("UPDATE Book SET quantity=? WHERE book_id=?;", (book["quantity"], book["book_id"],))
        # commit changes
        con.commit()
        db.close()
        con.close()
        # redirect to the main page
        session["cart"] = []
        flash("Order has been placed successfully")
        return redirect("/")

# admin 
# add book
## all books
## requests for books/updates
## requests for writers
## all users (email, state, button to change state)
## history


if __name__ == '__main__':
    app.run(debug=True)