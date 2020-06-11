import os

from flask import Flask, session, render_template, redirect, abort, url_for, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from . import auth_tool

app = Flask(__name__)
app.config.from_pyfile('../config.py')
credentials=os.getenv("PSQL_CREDS")
engine = create_engine(credentials+"web50")
db = scoped_session(sessionmaker(bind=engine))
@app.context_processor
def display_year_c():
	from time import strftime
	return dict(show_year="© 2020-"+strftime("%Y"))



Session(app)

@app.route('/')
def index():
	if session.get('username') is None:
		return redirect(url_for('login'))
	else:
		return render_template('index.html',username=session.get('username'))

@app.route('/search',methods=["GET","POST"])
def search():
	result={}
	if request.method == "POST":
		title=request.form.get("book_title")
		if title is not None:
			result=db.execute("select * from books where title like :title",{'title':'%'+title+'%'}).fetchall()
	else:
		title=request.args.get("book_title")
		if title is not None:
			result=db.execute("select * from books where title like :title",{'title':'%'+title+'%'}).fetchall()

	return render_template("search.html",books=result)

@app.route('/review')
def review():
	pass

@app.route('/dashboard')
def dashboard():
	pass

@app.route('/browse')
def browse():
	pass

@app.route('/api/<isbn>',methods=["GET","POST"])
def get_isbn(isbn):
	#to make sure that the query doesn't open up to SQLi also there should only ever be one result.
	data=db.execute("select * from books where isbn = :isbn",{"isbn":isbn}).fetchone()
	if data is not None:
		output= {'isbn': data.isbn, 'title': data.title, 'author': data.author, 'year': data.published_year,
				 'review_count': data.total_reviews,
				 #if the average score is still set at 0.0 then we return 0 as to not get a divide by zero error.
				 'average_score': (data.total_review_score / data.total_reviews) if data.total_reviews > 0 else 0}
		# craft our response.
		response = app.make_response(output)
		# make sure it's stated that it's pure JSON.
		response.mimetype = "application/json"
		# return that data.
		return response
	#if it's no found redirect them to 404 page.
	else:
		#return redirect(url_for("error_404"),code=404)
		abort(404)

@app.route('/404')
def error_404():
	return "Page not found"

@app.route('/test')
def test():
	return str(current_app.config['PEPPER'])

@app.route('/login',methods=["GET","POST"])
def login():
	#see what type of request it is.
	if request.method == "GET":
		#if it's a get request just return the form like normal.
		return render_template('login.html')
	else:
		#get the static pepper that's used for the entire thing and never ever changes.
		pepper=app.config['PEPPER']
		#get the username from the form.
		username=request.form.get('username')
		#the password.
		password=request.form.get('password')
		#modify the password mobilzed(e.g. first char is letter uppercase it otherwise keep it the same)
		mobile_password=password[0].upper()+password[1:]
		#only get a single result there should only ever be one. Also not selecting all as we dont' need all data.
		result=db.execute('Select password,mobile_password from users where username = :username',{'username':username}).fetchone()
		#if it's none then they don't exist.
		if result is not None:
			#check their normal password.
			pass_good = auth_tool.verify_password(password, pepper, result.password)
			#if it's passed
			if pass_good :
				#they are authorized. Later we'll redirect them.
				msg="authorized"
				#setup the session variable username.
				session['username'] = username
			#else we see if the mobile version of the password works.
			else:
				#see if the mobile version of teh password works.
				pass_good= auth_tool.verify_password(mobile_password, pepper, result.mobile_password)
				#if that's OK then they have a good password.
				if pass_good:
					session['username'] = username
					#this is just debug.
					msg="authorized mobile"
				#otherwise neither worked and they are denied.
				else:
					msg="denied"
			return render_template("login.html",msg=msg)
		else:
			return render_template("login.html",msg="failed")

@app.route('/register',methods=["GET","POST"])
def register():
	if request.method == "POST":
		pepper=app.config['PEPPER']
		username=request.form.get('username')
		if username is None:
			return render_template('register.html', msg="No username specified")

		if db.execute('select id from users where username=:username',{'username':username}).fetchone() is not None:
			return render_template('register.html', msg="error user already exists")
		else:
			password=request.form.get('password')
			if passowrd is None:
				return render_template("register.html",msg="No password specified")
			mobile_password=password[0].upper()+password[1:]

			password=auth_tool.hash_password(password, pepper)
			mobile_password= auth_tool.hash_password(mobile_password, pepper)
			db.execute('INSERT INTO USERS(username,password,mobile_password) VALUES (:username,:password,:mobile_password)',{'username':username,'password':password,'mobile_password':mobile_password})
			db.commit()
			return redirect(url_for("index"))
	else:
		return render_template('register.html', msg="")

@app.route('/logout')
def logout():
	pass

@app.route('/books')
def books():
	books1=db.execute("SELECT * from books").fetchall()
	return render_template('books.html', books=books1)
if __name__ == '__main__':
	app.run()

@app.route('/logged_in')
def logged_in():
	if 'username' in session:
		return "logged in as %s" % session['username']
	return 'you are not logged in'