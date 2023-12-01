## Data Base Schema
``` SQL
-- create a table for user state
CREATE TABLE IF NOT EXISTS User_State(
  state_id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT
);
-- create a table for users
CREATE TABLE IF NOT EXISTS User(
	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	full_name TEXT NOT NULL,
  	email TEXT NOT NULL UNIQUE,
  	password TEXT NOT NULL,
  	admin_state_id INTEGER,
  	FOREIGN KEY (admin_state_id) REFERENCES User_State(state_id)
);
-- create a table for categories
CREATE TABLE IF NOT EXISTS Category(
	category_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	title TEXT NOT NULL
);
-- create a table for book's tags
CREATE TABLE IF NOT EXISTS Tag(
	tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	title TEXT NOT NULL,
  	state INTEGER DEFAULT 0 CHECK(state <= 1 AND state >= 0)
);
-- create a table for books
CREATE TABLE IF NOT EXISTS Book(
	book_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	title TEXT NOT NULL,
  	author TEXT,
  	image TEXT,
  	price REAL NOT NULL,
  	subscript TEXT,
  	quantity INTEGER NOT NULL,
  	state INTEGER NOT NULL DEFAULT 0,
  	writer_id INTEGER,
  	category_id INTEGER,
  	FOREIGN KEY (writer_id) REFERENCES User(user_id),
  	FOREIGN KEY (category_id) REFERENCES Category(category_id)
);
-- create a table to ralate a book with its tags
CREATE TABLE IF NOT EXISTS Book_Tag(
	tag_id INTEGER,
  	book_id INTEGER,
  	FOREIGN KEY (tag_id) REFERENCES Tag(tag_id),
  	FOREIGN KEY (book_id) REFERENCES Book(book_id),
  	PRIMARY KEY(tag_id,book_id)
);
-- create a table for bills
CREATE TABLE IF NOT EXISTS Bill(
	bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	user_id INTEGER,
  	total REAL,
    address TEXT NOT NULL,
  	phone TEXT NOT NULL,
  	data_time TEXT,
  	FOREIGN KEY (user_id) REFERENCES User(user_id)
);
-- create a table to place an order
CREATE TABLE IF NOT EXISTS Book_Order(
	order_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	book_id INTEGER,
  	bill_id INTEGER,
  	price_per_book REAL,
  	quantity INTEGER NOT NULL,
  	FOREIGN KEY (book_id) REFERENCES Book(book_id),
  	FOREIGN KEY (bill_id) REFERENCES Bill(bill_id)
);
-- create a table for book reviews
CREATE TABLE IF NOT EXISTS Review(
	user_id INTEGER,
  	book_id INTEGER,
  	data_time TEXT,
  	content TEXT,
  	rate INTEGER,
  	FOREIGN KEY (user_id) REFERENCES User(user_id),
  	FOREIGN KEY (book_id) REFERENCES Book(book_id),
  	PRIMARY KEY(user_id,book_id)
);
```
