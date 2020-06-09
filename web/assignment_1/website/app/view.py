import os

from app import app
from flask import current_app
from flask import render_template, redirect, url_for, abort, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

credentials=os.getenv("PSQL_CREDS")
from . import auth_tool
engine = create_engine(credentials+"web50")
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
	return render_template('index.html')
	#return app.config['SQL_CREDENTIALS']

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
	if request.method == "GET":
		return render_template('login.html')
	else:
		pepper=app.config['PEPPER']
		username=request.form.get('username')
		password=request.form.get('password')
		mobile_password=password[0].upper()+password[1:]

		result=db.execute('Select password,mobile_password from users where username = :username',{'username':username}).fetchone()
		if result is not None:
			pass_good = auth_tool.verify_password(password,pepper,result.password)
			if(pass_good):
				msg="authorized"
			else:
				pass_good=auth_tool.verify_password(mobile_password,pepper,result.mobile_password)
				if(pass_good):
					msg="authorized mobile"
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
		if db.execute('select id from users where username=:username',{'username':username}).fetchone() is not None:
			return render_template('register.html', msg="error user already exists")
		else:
			password=request.form.get('password')
			mobile_password=password[0].upper()+password[1:]
			password=auth_tool.hash_password(password,pepper)
			mobile_password=auth_tool.hash_password(mobile_password,pepper)
			db.execute('INSERT INTO USERS(username,password,mobile_password) VALUES (:username,:password,:mobile_password)',{'username':username,'password':password,'mobile_password':mobile_password})
			db.commit()
			return redirect(url_for("index"))
	else:
		return render_template('register.html', msg="")


@app.route('/books')
def books():
	books1=db.execute("SELECT * from books").fetchall()
	return render_template('books.html', books=books1)
if __name__ == '__main__':
	app.run()
