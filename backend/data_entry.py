import os
import requests
from urllib.parse import quote
from PIL import Image
from io import BytesIO
import sqlite3
import random

def download_and_convert_image(url, format='jpg', folder_path='static/DBimages', bookid=None):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Encode the URL
    encoded_url = quote(url, safe=':/')

    # Extract the image name from the encoded URL
    image_name = os.path.join(folder_path, f'{bookid}.{format}')

    # Download the image
    response = requests.get(url)
    image_data = BytesIO(response.content)

    # Convert the image format if needed
    if format.lower() not in ('jpg', 'jpeg', 'png'):
        raise ValueError("Unsupported image format. Supported formats: 'jpg', 'jpeg', 'png'")
    elif format.lower() != 'jpg':
        img = Image.open(image_data)
        img.save(image_name, format=format.upper())
    else:
        with open(image_name, 'wb') as f:
            f.write(response.content)

    # Return the local path of the saved image
    return image_name

# Example usage:
con = sqlite3.connect('Books.db')
db = con.cursor()
db.execute("SELECT * FROM Category")
columns = [column[0] for column in db.description]
categories = [dict(zip(columns, row)) for row in db.fetchall()]
for category in categories:
    option = category['title']
    url = f'https://www.googleapis.com/books/v1/volumes?q={option}&keys:key=AIzaSyAL46FdWUJnKPTP9_yeYRD6IzkqpvMSjvE'
    response = requests.get(url)
    data = response.json()
    for book in data['items']:
        bookid = book['id']
        title = book['volumeInfo']['title']
        if('authors' not in book['volumeInfo']):
            author = 'Unknown'
        else:
            author = book['volumeInfo']['authors'][0]
        if('description' not in book['volumeInfo']):
            description = 'No description'
        else:
            description = book['volumeInfo']['description']
        try:
            image_url = book['volumeInfo']['imageLinks']['thumbnail']
            local_path = download_and_convert_image(image_url, format='png', bookid=bookid)
        except:
            image_url = f'https://www.placehold.it/200x300/EFEFEF/AAAAAA&text={title}'
            local_path = download_and_convert_image(image_url, format='png', bookid=bookid)
        price = random.randint(20, 500)
        quantity = random.randint(10, 100)
        category_id = category['category_id']
        writer_id = 1;
        state=1;
        # store image local path in database
        db.execute("INSERT INTO Book (title, author, subscript, image, price, quantity, category_id, writer_id, state) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (title, author, description, local_path, price, quantity, category_id, writer_id, state))
        con.commit()

image_url = 'https://books.google.com/books/content?id=UwVnDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'
local_path = download_and_convert_image(image_url, format='png')

print(f"The image has been saved locally at: {local_path}")
