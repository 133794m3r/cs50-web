# Book Reviewers
A basic site where you can leave reviews, and also get reviews includes an API.

## Youtube Video
(Youtube Demo)[https://www.youtube.com/watch?v=jfqE9EjYJ-g]

## Features Required
- Registration: Users should be able to register for your website, providing (at minimum) a username and password.
- Login: Users, once registered, should be able to log in to your website with their username and password.
- Logout: Logged in users should be able to log out of the site.
- Import: Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called import.py separate from your web application, write a program that will take the books and import them into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python3 import.py to import the books into your database, and submit this program with the rest of your project code.
- Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
- Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
- Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
- Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
- API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:
# app
This folder contains most of the main code.

## tempplates
This contains the templates various pages.
### book.html
This contains the single book viewer template.
### dashboard.html
The "dashboard" that contains the user's reviews if they're logged in.
### index.html
The main page that the user sees upon visiting the site.
### layout.html
This is the basic page skeleton. It contains all of the basic items.
### register.html
This is the register page. It has the user try to create a username, and also select a password. They also have to select the "I agree" but it is just for show. Also it scores the password using zxcvbn scoring system. https://github.com/dropbox/zxcvbn I've personally been using it for years on all projects I'm a part of.
It blocks them from registering until their password's strength is at least a 1 out of 4 on the scoring system, and also suggests to them ways to make it stronger.

### review.html
This is the review page where the user can see any review by it's id or they can edit their own review. If they submit their data it's updated in the server and the information is shown to them.

## static
This folder contains the bootstrap files, and also the zxcvbn soure code.

## auth_toool.py
This python module contains my password hasher and also the verifier. It uses scrypt for the hashing function, and also packs the data into a struct. It uses a random salt and also an application specific pepper.

### functions 
- verify_password It verifies the user's password with the supplied hash.
- hash_password It will hash the user's password with scrypt then pack it into a base64 encoded string. Each password has a unique salt, and an application unique pepper.

## view.py
This file contains _all_ of the routes. It also had template filters, global variables, sessions, and also the database queries that are needed. It's the main file of the project.

## lib.py
This file contains the following functions.
### functions
- dict_proxy This function takes a SQLAlchemy ResultProxy and converts into a dict.
- gr_search This function queries the GoodReads API and gets back the average review score and total number of reviews.
- get_reviews This function gets all of the reviews from the database and returns a dict of that data. It also converts the timestamps from native python format to a UTC string version.


## books.csv
The book file that was given to us.
## importer.py
This is the file that'll import the CSV file into the Postgres Database

## config.py
This contains the configurations for the flask application and also sets up the variables for the app itself.

## data
This folder contains the tables exported as SQL files so that you can reimport it.

# requirements
- requests==2.20.0
- Flask==1.1.2
- scrypt==0.8.15
- SQLAlchemy==1.2.19
- Flask-Session==0.3.2
- pycryptodome==3.9.7

The requirements.txt file also includes this information.
