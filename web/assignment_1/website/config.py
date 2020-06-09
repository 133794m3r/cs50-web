
import os
DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#not used right now.
CSRF_ENABLED    = True
#The pepper we're going to use.
PEPPER = os.getenv("FLASK_PEPPER")
#Not used right now but would be if I was doing CRSF protection.
CSRF_SESSION_KEY = os.getenv("CRSF_SESSION_KEY")
#Same here for session cookies.
SECRET_KEY = os.getenv("SECRET_KEY")
#to get my GoodReads API Key.
GR_API_KEY = os.getenv("GR_API_KEY")