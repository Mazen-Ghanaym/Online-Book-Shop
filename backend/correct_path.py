import os
import requests
from urllib.parse import quote
from PIL import Image
from io import BytesIO
import sqlite3
import random

con = sqlite3.connect('Books.db')
db = con.cursor()
db.execute("SELECT * FROM Book")
columns = [column[0] for column in db.description]
books = [dict(zip(columns, row)) for row in db.fetchall()]
for book in books:
    print(f"{book['image']}")
    image_url = book['image']
    image_urt = image_url.replace('/', '\\')
    print(f"{image_urt}")
    db.execute("UPDATE Book SET image = ? WHERE book_id = ?", (image_urt, book['book_id']))
    con.commit()

