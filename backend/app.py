import os
import datetime
from pydoc import cram
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


# session["cart"] = {} # {book_id: quantity}
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin")
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
    rows = [dict(zip(cols_disc, row)) for row in db_fetch]
    return rows


def getQuaryFromDataBase(database="Books.db", quary_text="", *args):
    # make a connect with the database
    con = sqlite3.connect(database)
    # create cursor with called db
    db = con.cursor()
    con.row_factory = sqlite3.Row
    # try to get the data
    try:
        db.execute(quary_text, tuple(args))
        data = getData(db.fetchall(), db.description)
        con.commit()
        db.close()
        con.close()
    except:
        return None
    return data


def createErrorMessage(err_state=False, err_type=None, err_mesg_txt=None):
    error_message = {
        "error_state": err_state,
        "error_type": err_type,
        "error_message_text": err_mesg_txt,
    }
    return error_message


def validEmail(the_email):
    if the_email == None:
        return False
    # todo you need to select all emails from the data base to check that email is not found
    else:
        all_emails = getQuaryFromDataBase(
            "Books.db",
            "select email from user where user_id <> ?",
            session["user_id"],
        )
        just_emails = [row["email"] for row in all_emails]
        return the_email not in just_emails


def validName(the_name):
    if the_name == None:
        return False
    else:
        return True


def correctImage(imagePath):
    return "..\\" + str(imagePath).replace("/", "\\")


# ----------------------------------------------------------------------------------------


# login  -> mazen
@app.route("/signin", methods=["GET", "POST"])
def signin():
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
            return render_template("signin.html", error_message="message", invalid=True)
        # Ensure password was submitted
        elif not password:
            return render_template("signin.html", error_message="message", invalid=True)
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # Query database for username
        db.execute("SELECT * FROM User WHERE email = ?", (email,))
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        rows = [dict(zip(columns, row)) for row in db.fetchall()]

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return render_template("signin.html", error_message="message", invalid=True)

        if rows[0]["password"] != password:
            return render_template("signin.html", error_message="message", invalid=True)

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
        return render_template("signin.html", error_message="", invalid=False)


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
            return render_template(
                "signup.html", error_message="message email", invalid=True
            )

        # check if user provide valid password
        if not password:
            return render_template(
                "signup.html", error_message="message password", invalid=True
            )

        # check if user provide valid confirm
        if not confirm:
            return render_template(
                "signup.html", error_message="message confirm", invalid=True
            )

        # check if password equals the confirmation password
        if password != confirm:
            return render_template("signup.html", error_message="message", invalid=True)
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
        user_state = db.execute(
            "SELECT * FROM User_state WHERE title = ?;", ("user",)
        ).fetchone()
        db.execute(
            "INSERT INTO User(email,full_name,password,admin_state_id) VALUES(?,?,?,?);",
            (
                email,
                fullname,
                password,
                user_state[0],
            ),
        )
        # retrive new user id from database
        db.execute("SELECT * FROM User WHERE email=?", (email,))

        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        registrant = [dict(zip(columns, row)) for row in db.fetchall()]

        # add user id to session
        session["user_id"] = registrant[0]["user_id"]

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
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    # change password
    if request.method == "POST":
        if validEmail(request.form.get("email")):
            pass
        else:
            pass
        if validName(request.form.get("name")):
            pass
        else:
            pass
        # update the user info in database
        # quary of update
        return redirect(url_for(profile))

    # show profile
    else:
        personInfo = getQuaryFromDataBase(
            "Books.db",
            "select * from user where user_id = ?",
            int(session["user_id"]),
        )
        # render_template(
        # "profile.html",
        # err_mes = createErrorMessage(),
        # personInfo = personInfo
        # )
        return render_template(
            "layout.html",
            page_name="profile",
            err_mes=createErrorMessage(),
            items=personInfo,
        )


# home
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    """Show home page"""
    if request.method == "GET":
        session["cart"] = {}

        # display all categories with their books
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # retrive all categories from database
        db.execute("SELECT * FROM Category;")
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        categories = [dict(zip(columns, row)) for row in db.fetchall()]
        # retrive first 5 books
        # print(categories)
        db.execute("SELECT * FROM Book WHERE state=? LIMIT 5;", (1,))
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        popular_books = [dict(zip(columns, row)) for row in db.fetchall()]
        # retrive all books from database with state = 1 and each category with their books in dictionary
        for category in categories:
            db.execute(
                "SELECT * FROM Book WHERE category_id=? AND state=? LIMIT 5;",
                (
                    category["category_id"],
                    1,
                ),
            )
            # convert retrived data into list of dictionaries
            columns = [column[0] for column in db.description]
            category["books"] = [dict(zip(columns, row)) for row in db.fetchall()]
        # commit changes
        con.commit()
        db.close()
        con.close()
        # render home page
        # TODO: popular books
        # print(categories)
        return render_template(
            "home.html", categories=categories, popular_books=popular_books
        )
    else:
        # retrive data from form
        search = request.form.get("search")
        # TODO:


# library for search books
@app.route("/library", methods=["GET", "POST"])
@app.route("/library/<category_id>", methods=["GET", "POST"])
def library(category_id=None):
    """Show library page"""
    if request.method == "GET":
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # retrive all categories from database
        db.execute("SELECT * FROM Category;")
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        categories = [dict(zip(columns, row)) for row in db.fetchall()]

        if category_id == None:
            # retrive all books from database with state = 1
            db.execute("SELECT * FROM Book WHERE state=?", (1,))
            # convert retrived data into list of dictionaries
            columns = [column[0] for column in db.description]
            books = [dict(zip(columns, row)) for row in db.fetchall()]
            # commit changes
            con.commit()
            db.close()
            con.close()
            # render library page
            return render_template(
                "library.html", books=books, categories=categories, search="All Books"
            )
        else:
            # retrive all books from database with the same category_id
            db.execute(
                "SELECT * FROM Book WHERE category_id = ? AND state = ?;",
                (
                    category_id,
                    1,
                ),
            )
            # convert retrived data into list of dictionaries
            columns = [column[0] for column in db.description]
            books = [dict(zip(columns, row)) for row in db.fetchall()]
            # retrive all categories with category_id
            db.execute(
                "SELECT title FROM Category WHERE category_id = ?;",
                (category_id,),
            )
            # convert retrived data into list of dictionaries
            columns = [column[0] for column in db.description]
            category = [dict(zip(columns, row)) for row in db.fetchall()]
            # commit changes
            con.commit()
            db.close()
            con.close()
            # render library page
            return render_template(
                "library.html",
                books=books,
                categories=categories,
                search=category[0]["title"],
            )
    else:
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # retrive all categories from database
        db.execute("SELECT * FROM Category;")
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        categories = [dict(zip(columns, row)) for row in db.fetchall()]
        # retrive data from form
        if category_id == None:
            search = request.form.get("search")
            # retrive all books from database like search title
            db.execute(
                "SELECT * FROM Book WHERE title LIKE ? AND state = ?;",
                (
                    "%" + search + "%",
                    1,
                ),
            )
            # convert retrived data into list of dictionaries
            columns = [column[0] for column in db.description]
            books = [dict(zip(columns, row)) for row in db.fetchall()]
            # commit changes
            con.commit()
            db.close()
            con.close()
            # render library page
            return render_template(
                "library.html", books=books, categories=categories, search=search
            )


# book -> mahmoud
@app.route("/book/<int:bookId>", methods=["GET", "POST"])
@login_required
def book(bookId):
    # get data from  database with the quary below
    # ! ------------------------------------------
    bookInfo = getQuaryFromDataBase(
        "Books.db",
        "select * from Book where book_id = ?",
        bookId,
    )
    if bookInfo != None and len(bookInfo) != 1:
        return redirect(url_for("home"))
    else:
        bookInfo = bookInfo[0]

    bookInfo["image"] = correctImage(bookInfo["image"])
    similarBookInfo = getQuaryFromDataBase(
        "Books.db",
        "select * from Book where category_id = ? LIMIT 4",
        bookInfo["category_id"],
    )
    quantityOfBook = 0

    def getQuantity(bId):
        quantity = 0
        try:
            quantity = int(session["cart"][bId])
        except:
            quantity = 0
        print(quantity)
        return quantity

    # ! ------------------------------------------
    # if user wants to add an item to their cart
    if request.method == "POST":
        # handling
        if session.get("user_id") == None:
            error_message = createErrorMessage(
                True,
                "login_required",
                "You have to login fisrt to be able to buy this item.",
            )
            return render_template("signin.html", err_mes=error_message)

        # handling the quantity error when quantity be non positive value
        if int(request.form.get("quantity")) < 1:
            return render_template(
                "book.html",
                bookInfo=bookInfo,
                quantity=quantityOfBook,
                simBooks=similarBookInfo,
                err_mes=createErrorMessage(
                    True, "invaled value", "Quantity can not be non positive!"
                ),
            )

        # check if these is any item in the cart before (cart has been created)

        if session.get("cart"):  # if cart already created
            session["cart"][bookId] = int(request.form.get("quantity"))
        else:  # if cart not created
            session["cart"] = {}  # cart will be a dict
            session["cart"][bookId] = int(request.form.get("quantity"))
        # try to get the quantity of the book from the session.
        # quantityOfBook = getQuantity(bookId)
        try:
            quantityOfBook = int(session["cart"][bookId])
        except:
            quantityOfBook = 0
        return redirect(url_for("book", bookId=str(bookId)))
        # return render_template("book.html",
        #                        bookInfo=bookInfo,
        #                        quantity=quantityOfBook,
        #                        simBooks=similarBookInfo,
        #                        err_mes=createErrorMessage()
        #                        )

    # if the user request the page via "get" method
    else:
        return render_template(
            "book.html",
            bookInfo=bookInfo,
            quantity=quantityOfBook,
            simBooks=similarBookInfo,
            err_mes=createErrorMessage(),
        )


# cart -> mazen
# session["cart"] = []
@app.route("/cart/add/<book_id>", methods=["GET", "POST"])
@login_required
def add_to_cart(book_id):
    """Add book to cart"""
    # connect with database and create cursor called db
    con = sqlite3.connect("Books.db")
    db = con.cursor()
    quantity = 1
    # check whether the quantity submitted from book page(has quantity) or from library page(doesn't has quantity)
    try:
        quantity = int(request.form.get("quantity"))
    except ValueError:
        return "TODO"

    # retrive all books from database with the same book_id
    db.execute(
        "SELECT * FROM Book WHERE book_id = ? AND state = ?;",
        (
            book_id,
            1,
        ),
    )

    # convert retrived data into list of dictionaries
    columns = [column[0] for column in db.description]
    books = [dict(zip(columns, row)) for row in db.fetchall()]

    # add book to cart
    session["cart"][books[0]["book_id"]] = quantity

    # commit changes
    con.commit()
    db.close()
    con.close()

    # redirect to the main page
    return redirect("/cart")


@app.route("/cart/remove/<book_id>", methods=["GET", "POST"])
@login_required
def remove_from_cart(book_id):
    """Remove book from cart"""
    if request.method == "GET":
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # retrive all books from database with the same book_id
        db.execute(
            "SELECT * FROM Book WHERE book_id = ? WHERE state = ?;",
            (
                book_id,
                1,
            ),
        )

        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        books = [dict(zip(columns, row)) for row in db.fetchall()]

        # remove book from cart
        session["cart"].pop(books[0]["book_id"])

        # commit changes
        con.commit()
        db.close()
        con.close()

        # redirect to the main page
        return redirect("/cart")
    else:
        # I don't know what to do here
        return "TODO"


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    """Show cart"""
    if request.method == "GET":
        # retrive all books from database with the same book_id
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()

        # retrive all books from database with the same book_id
        # keys is a tuple of book_id after converting session["cart"] to tuple
        keys = tuple(session["cart"].keys())
        # place = ?,?,?... as the number of keys
        place = ",".join("?" * len(keys))
        # add state = 1 to keys
        keys = keys + (1,)
        db.execute(
            f"SELECT * FROM Book WHERE book_id IN ({place}) AND state = ?;", (keys)
        )
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        books = [dict(zip(columns, row)) for row in db.fetchall()]
        # update quantity in books
        for book in session["cart"].keys():
            books[book]["quantity"] = session["cart"][book]
        # commit changes
        con.commit()
        db.close()
        con.close()
        # render cart page
        return render_template(
            "cart.html", books=books, error_message="", invalid=False
        )
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
        # retrive original books from database
        # keys is a tuple of book_id after converting session["cart"] to tuple
        keys = tuple(session["cart"].keys())
        # place = ?,?,?... as the number of keys
        place = ",".join("?" * len(keys))
        # add state = 1 to keys
        keys = keys + (1,)
        db.execute(
            f"SELECT * FROM Book WHERE book_id IN ({place}) AND state = ?;", (keys)
        )
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        books = [dict(zip(columns, row)) for row in db.fetchall()]
        # each book in session["cart"] has {book_id : quantity}
        # ! I think about error why
        # ! while i'm updating the book['quantity'] in session["cart"] if i found an error
        # ! and i returned the user if he want to change the quantity of the book
        # ! when compare we will compare with the updated quantity(from prevous request) not the original quantity(in database)
        # copy books to new_books for updating quantity in new_books
        new_books = books
        # update quantity in new_books
        for book in session["cart"].keys():
            new_books[book]["quantity"] = session["cart"][book]

        # retrive new quantity from form for each book
        for book_id in session["cart"].keys():
            # quantity_name = quantity_[book_id] this name will be the same as the name of the input in cart.html form
            quantity_name = "quentity_" + str(book_id)
            # retrive new quantity from form
            new_quantity = request.form.get(quantity_name)
            # check if new quantity is valid
            try:
                new_quantity = int(new_quantity)
            except ValueError:
                return render_template(
                    "cart.html", cart=new_books, error_message="message", invalid=True
                )
            # check if new quantity is valid
            if new_quantity < 0:
                return render_template(
                    "cart.html", cart=new_books, error_message="message", invalid=True
                )
            # check if new quantity is valid
            if new_quantity > books[book_id]["quantity"]:
                return render_template(
                    "cart.html", cart=new_books, error_message="message", invalid=True
                )
            # update quantity in session["cart"]
            session["cart"][book_id] = new_quantity
            # update quantity in database
            total += new_quantity * books[book_id]["price"]

        # check if total is valid with user balance
        """TODO"""

        # insert into bill table first
        db.execute(
            "INSERT INTO Bill(address, phone, user_id, date_time, total) VALUES(?,?,?,?);",
            (
                address,
                phone,
                user_id,
                date_time,
                total,
            ),
        )
        # retrive bill id from database
        db.execute(
            "SELECT * FROM Bill WHERE user_id=? AND date_time=?;",
            (
                user_id,
                date_time,
            ),
        )
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        bills = [dict(zip(columns, row)) for row in db.fetchall()]

        bill_id = bills[0]["bill_id"]
        # insert into order table they have same bill
        for book in session["cart"]:
            db.execute(
                "INSERT INTO Order(bill_id, book_id, quantity, price_per_book) VALUES(?,?,?,?);",
                (
                    bill_id,
                    book["book_id"],
                    book["quantity"],
                    book["price"],
                ),
            )
        # update quantity in database
        for book in session["cart"].keys():
            # old quantity
            db.execute(
                "SELECT quantity FROM Book WHERE book_id = ?;",
                (book,),
            )
            # convert retrived data into list of dictionaries
            columns = [column[0] for column in db.description]
            books = [dict(zip(columns, row)) for row in db.fetchall()]
            old_quantity = books[0]["quantity"]
            db.execute(
                "UPDATE Book SET quantity = ? WHERE book_id = ?;",
                (
                    old_quantity - session["cart"][book],
                    book,
                ),
            )
        # commit changes
        con.commit()
        db.close()
        con.close()
        # redirect to the main page
        session["cart"] = {}
        flash("Order has been placed successfully")
        return redirect("/")


# save quantity changes in cart
@app.route("/cart/save", methods=["GET", "POST"])
@login_required
def save_cart():
    """Save cart"""
    if request.method == "POST":
        # connect with database and create cursor called db
        con = sqlite3.connect("Books.db")
        db = con.cursor()
        # retrive original books from database
        db.execute(
            "SELECT * FROM Book WHERE book_id IN (?) AND state = ?;",
            (
                session["cart"].keys(),
                1,
            ),
        )
        # convert retrived data into list of dictionaries
        columns = [column[0] for column in db.description]
        books = [dict(zip(columns, row)) for row in db.fetchall()]
        # each book in session["cart"] has {book_id : quantity}
        # copy books to new_books for updating quantity in new_books
        new_books = books
        # update quantity in new_books
        for book in session["cart"].keys():
            new_books[book]["quantity"] = session["cart"][book]

        # retrive new quantity from form for each book
        for book_id in session["cart"].keys():
            # quantity_name = quantity_[book_id] this name will be the same as the name of the input in cart.html form
            quantity_name = "quentity_" + str(book_id)
            # retrive new quantity from form
            new_quantity = request.form.get(quantity_name)
            # check if new quantity is valid
            try:
                new_quantity = int(new_quantity)
            except ValueError:
                return render_template(
                    "cart.html", cart=new_books, error_message="message", invalid=True
                )
            # check if new quantity is valid
            if new_quantity < 0:
                return render_template(
                    "cart.html", cart=new_books, error_message="message", invalid=True
                )
            # check if new quantity is valid
            if new_quantity > books[book_id]["quantity"]:
                return render_template(
                    "cart.html", cart=new_books, error_message="message", invalid=True
                )
            # update quantity in session["cart"]
            session["cart"][book_id] = new_quantity
            # update quantity in database
        redirect("/cart")


# admin
# add book
## all books
## requests for books/updates
## requests for writers
## all users (email, state, button to change state)
## history


if __name__ == "__main__":
    app.run(debug=True)
