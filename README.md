# Bookstore Management System

This is a **Bookstore Management System** built using Python, Flask, and SQLite. The system allows users to manage books, users, and orders through a graphical user interface (GUI). It includes features such as adding/updating books, managing user accounts, processing orders, and generating bills.

## Contributors

- [Mahmoud Sameh](https://github.com/MhmudSameh24)
- [Mazen Ghanayem](https://github.com/Mazen-Ghanaym)
- [Youssef Gaber](https://github.com/Yousef-Gaber11)
- [Hamza Hassanain](https://github.com/HamzaHassanain)
- [Islam Imad](https://github.com/Islam-Imad)
- [Mohamed Mahmoud](https://github.com/mohammedmoud)

## Features

- **User Authentication**: Users can sign up, log in, and manage their profiles.
- **Book Management**: Admins can add, update, and delete books.
- **Order Management**: Users can add books to their cart, place orders, and view order history.
- **Search and Filter**: Users can search for books and filter by categories.
- **Responsive Design**: The application is designed to work on both desktop and mobile devices.

### UI/UX

- [**Figma**](https://www.figma.com/file/6bupK25j6M0cs0giEcgNFY/BookShop?type=design&node-id=0%3A1&mode=design&t=T7BOsjL3jJpPWLuU-1)

### Database

- [**Physical Data Model**](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Book_Shop.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1hHyepPb6qJTHaLV6itX-jHsstqGLPB9j%26export%3Ddownload)

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.x**: The project is written in Python. You can download it from [python.org](https://www.python.org/downloads/).
- **SQLite**: The database used in this project. It comes pre-installed with Python.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Mazen-Ghanaym/Online-Book-Shop
   cd Online-Book-Shop
   ```

2. **Install required packages**:
   The project uses the following Python packages:
   - `Flask`
   - `Flask-Session`
   - `sqlite3`

   To install the required packages, run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   - Run the `schema.sql` script to create the necessary tables in the SQLite database:

     ```bash
     sqlite3 Books.db < schema.sql
     ```

   - Optionally, you can populate the database with fake data using the `data_entry.py` script:

     ```bash
     python data_entry.py
     ```

## Running the Application

1. **Start the application**:
   Run the `app.py` file to start the application:

   ```bash
   python app.py
   ```

2. **Access the application**:
   Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. **Login**:
   - sign up as a new user.

4. **Navigate the application**:
   - **Home Page**: Browse books and add them to your cart.
   - **Profile Page**: Update your profile and view order history.
   - **Cart Page**: Review your cart, update quantities, and place orders.
   - **Admin Add Book Page**: Add (admin only).

## Project Structure

- **`app.py`**: The main Flask application file.
- **`schema.sql`**: SQL script to create the database schema.
- **`data_entry.py`**: Script to populate the database with sample data.
- **`templates/`**: Contains HTML templates for the web pages.
- **`static/`**: Contains CSS, JavaScript, and images for the frontend.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## Acknowledgments

- **Flask**: For providing the web framework.
- **SQLite**: For the lightweight database solution.
- **Font Awesome**: For the icons used in the project.
