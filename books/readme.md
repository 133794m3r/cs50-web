# Book Store
The project is organized in the normal stuff.

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
