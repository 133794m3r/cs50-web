import os

from flask import Flask, session, render_template, redirect, abort, url_for, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from . import auth_tool

app = Flask(__name__)
app.config.from_pyfile('../config.py')
credentials = os.getenv("PSQL_CREDS")
engine = create_engine(credentials + "web50")
db = scoped_session(sessionmaker(bind=engine))


from .lib import gr_search,get_reviews,dict_proxy

@app.context_processor
def display_year_c():
	from time import strftime
	return dict(show_year="© 2020-" + strftime("%Y"))

@app.context_processor
def inject_user():
	return dict(USERNAME=session.get('username'))

Session(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
def search():
	if not session.get('user_id'):
		return redirect(url_for('login'))

	if request.method == "POST":
		query = request.form.get("search_string")
		if query is not None:
			try:
				query = int(query)
				result = db.execute("select * from books where published_year = :year",{'year':query}).fetchall()
			except:
				query = '%' + query.title() + '%'
				#function(123)
				result = db.execute("select * from books where title like :query or isbn like :query or author like :query",
			                   {'query':query}).fetchall()
			db.commit()
		return render_template("search.html", books=result)
	else:
		return render_template("search.html",books='')


@app.route('/book/<isbn>',methods=["GET"])
def book(isbn):
	if not session.get('user_id'):
		return redirect(url_for('login'))

	data = {}
	if isbn is not None:
		#data = get_reviews(isbn)

		result = db.execute("select * from books where isbn = :isbn", {"isbn": isbn}).fetchone()
		if result is not None:
			#gr_avg,gr_ratings = gr_search(isbn, app.config.get('GR_API_KEY'))
			gr_avg=1;gr_ratings=1
			data = {'isbn': result.isbn, 'title': result.title, 'author': result.author, 'year': result.published_year,
			          'review_count': result.total_reviews,
			          # if the average score is still set at 0.0 then we return 0 as to not get a divide by zero error.
			          'average_score': (result.total_review_score / result.total_reviews) if result.total_reviews > 0 else 0}
			reviews = db.execute("""select reviews.review_score,reviews.review_text,reviews.reviewed_time,users.username
			 from reviews right join users on reviews.user_id = users.id where isbn = :isbn""",
			                     {"isbn": isbn}).fetchone()
			db.commit()
			result = {}
			if reviews:
				reviews = dict_proxy(reviews)

			data['gr_avg_rating']=gr_avg
			data['gr_total_ratings']=gr_ratings
			#reviews=get_reviews(isbn)

		else:
			abort(404)
	# if it's no found redirect them to 404 page.
	else:
		# return redirect(url_for("error_404"),code=404)
		abort(404)

	return render_template('book.html',book_data=data,reviews=reviews)


#TODO: Make it so that the selection-y bits are their own section(the book info that is). The rest of it will be just re-populated.
#they are going to leave a review. Or they're submitting their review.
@app.route('/review/',methods=["GET","POST"])
#this is in case they want to see a specific review by someone.
@app.route('/review/id/<int:review_id>',methods=["GET"])
@app.route('/review/isbn/<isbns>',methods=["GET"])
def review():
	if not session.get('user_id'):
		return redirect(url_for('login'))

	if request.method == "GET":
		isbns=request.args.get('isbn')
		review_id=request.args.get('id')
		result=None
		if review_id is None and isbns is None:
			return redirect(url_for('search'))
		if review_id is not None:
			#result=db.execute("select * from reviews where id=:id",{'id':id});
			reviews = db.execute("""select reviews.isbn,reviews.review_score,reviews.review_text,reviews.reviewed_time,users.username
			 from reviews right join users on reviews.user_id = users.id where id = :id""",
			                     {"id": review_id})
			#return str(id)
		if isbns is None:
			isbns=reviews.isbn

		data = db.execute("select * from books where isbn = :isbn", {"isbn": isbns}).fetchone()
		#db.commit()
		#data=dict_proxy(data)[0]
		data=dict(zip(data.keys(),data))
		data['avg_score'] = 0 if data['total_reviews'] == 0 else round(data['total_review_score']/data['total_reviews'],2)
		if result is not None:
			result=dict_proxy(result)

		return render_template('review.html',book_info=data,reviews=result)
	if request.method == "POST":
		queried=False
		#update the database with the new fields.
		#db.execute("update books set total_reviews = total_reviews + 1, total_review_score = total_review_score + :review_points;")
		isbn=request.form.get('isbn')
		review_id=request.form.get('id')
		review_text = request.form.get('review_text')
		review_score = request.form.get('review_score')
		if review_id is not None:
			db.execute("""UPDATE reviews set(review_score,review_text) = (:review_score,review_text) 
				where id= :id and user_id = :user_id""",{'id':review_id,'user_id':session.get('user_id')})
			db.execute("""UPDATE books set total_review_score = (select (:review_score-total_review_score) from books where isbn = :isbn) 
			where isbn = :isbn""",{'isbn':isbn,'review_score':review_score})
			db.session.commit()
		elif isbn is not None:
			user_id=session.get('user_id')
			rows=db.execute("""select isbn from reviews where user_id = :user_id and isbn = :isbn""",{'user_id':user_id,'isbn':isbn}).fetchone()
			if rows:
				id= db.execute("""UPDATE reviews set(review_score,review_text) = (:review_score,review_text) where 
					user_id = :user_id and isbn = :isbn returning id""",
				    {'review_score':review_score,'review_text':review_text,'user_id':user_id,'isbn':isbn})
				#db.session.commit()
			else:
				id=db.execute("""INSERT INTO reviews(review_score,review_text,isbn,user_id) 
					values(:review_score,:review_text,:isbn,:user_id) RETURNING id""",
				    {'review_score':review_score,'review_text':review_text,'isbn':isbn,'user_id':user_id})
				db.execute("""UPDATE books SET total_reviews = total_reviews + 1, 
				total_review_score = total_review_score + :review_score; where isbn=:isbn""",{'review_score':review_score,'isbn':isbn})
				#db.session.commit()
		else:
			pass
		db.commit()
	return render_template('review.html')

@app.route('/gr_review/<isbns>',methods=["GET"])
def gr_review(isbns):
	output={}
	gr_reviews = gr_search(isbns, app.config.get('GR_API_KEY'))
	output['gr_avg_rating'] = gr_reviews[0]
	output['gr_ratings'] = gr_reviews[1]
	return jsonify(output)

@app.route('/reviews/<isbns>',methods=["GET","POST"])
def book_info(isbns):
	if request.method == "POST":
		request.form.get("isbns")
	result={}
	if isbns is not None:
		data = db.execute("select * from books where isbn = :isbn", {"isbn": isbns})

		if data is None:
			return jsonify({'book': False, 'reviews': False})

		else:
			data = dict_proxy(data)[0]
			if data['total_reviews'] != 0:
				reviews=get_reviews(isbns)
			else:
				reviews=[]
			#gr_search(isbns,app.config.get('GR_API_KEY'))
			#gr_avg,gr_ratings = gr_search(isbns, app.config.get('GR_API_KEY'))
			gr_avg_rating=1
			gr_total_ratings=1
			data['gr_avg_rating']=gr_avg
			data['gr_total_ratings']=gr_ratings
			result['book']=data;result['reviews']=reviews
			return jsonify(result)

	else:
		return jsonify({'book': False, 'reviews': False})




@app.route('/dashboard')
def dashboard():
	pass


@app.route('/browse')
def browse():
	pass


@app.route('/api/<isbn>', methods=["GET", "POST"])
def get_isbn(isbn):
	if request.method == "POST":
		isbn=request.form.get("isbn")
	# to make sure that the query doesn't open up to SQLi also there should only ever be one result.
	data = db.execute("select * from books where isbn = :isbn", {"isbn": isbn}).fetchone()
	if data is not None:
		output = {'isbn': data.isbn, 'title': data.title, 'author': data.author, 'year': data.published_year,
		          'review_count': data.total_reviews,
		          # if the average score is still set at 0.0 then we return 0 as to not get a divide by zero error.
		          'average_score': (data.total_review_score / data.total_reviews) if data.total_reviews > 0 else 0}
		if data.total_reviews == 0:
			gr_reviews=gr_search(isbn,app.config.get('GR_API_KEY'))
			output['gr_avg_rating'] = gr_reviews[0]
			output['gr_ratings'] = gr_reviews[1]

		# craft our response.
		response = app.make_response(output)
		# make sure it's stated that it's pure JSON.
		response.mimetype = "application/json"
		# return that data.
		return response
	# if it's no found redirect them to 404 page.
	else:
		# return redirect(url_for("error_404"),code=404)
		abort(404)


@app.route('/404')
def error_404():
	return "Page not found"


@app.route('/test')
def test():
	return str(current_app.config['PEPPER'])


@app.route('/login', methods=["GET", "POST"])
def login():
	# see what type of request it is.
	if request.method == "GET":
		# if it's a get request just return the form like normal.
		return render_template('login.html')
	else:
		# get the static pepper that's used for the entire thing and never ever changes.
		pepper = app.config['PEPPER']
		# get the username from the form.
		username = request.form.get('username')
		# the password.
		password = request.form.get('password')
		# modify the password mobilzed(e.g. first char is letter uppercase it otherwise keep it the same)
		mobile_password = password[0].upper() + password[1:]
		# only get a single result there should only ever be one. Also not selecting all as we dont' need all data.
		result = db.execute('Select password,mobile_password,id from users where username = :username',
		                    {'username': username}).fetchone()
		db.commit()
		# if it's none then they don't exist.
		if result is not None:
			# check their normal password.
			pass_good = auth_tool.verify_password(password, pepper, result.password)
			# if it's passed
			if not pass_good:
				# see if the mobile version of teh password works.
				pass_good = auth_tool.verify_password(mobile_password, pepper, result.mobile_password)
				# if that's OK then they have a good password.

			if pass_good:
				session['username']=username
				session['user_id']=result.id
				return redirect(url_for('index'))
			else:
				return render_template('login.html',msg="Password or Username Failed")
		else:
			return render_template("login.html", msg="failed")


@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		pepper = app.config['PEPPER']
		username = request.form.get('username')
		if username is None:
			return render_template('register.html', msg="No username specified")

		if db.execute('select id from users where username=:username', {'username': username}).fetchone() is not None:
			return render_template('register.html', msg="error user already exists")
		else:
			password = request.form.get('password')
			if passowrd is None:
				return render_template("register.html", msg="No password specified")
			mobile_password = password[0].upper() + password[1:]

			password = auth_tool.hash_password(password, pepper)
			mobile_password = auth_tool.hash_password(mobile_password, pepper)
			db.execute(
				'INSERT INTO USERS(username,password,mobile_password) VALUES (:username,:password,:mobile_password)',
				{'username': username, 'password': password, 'mobile_password': mobile_password})
			db.commit()
			return redirect(url_for("index"))
	else:
		return render_template('register.html', msg="")


@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))
	#pass


@app.route('/books')
def books():
	books1 = db.execute("SELECT * from books").fetchall()
	return render_template('books.html', books=books1)

@app.route('/logged_in')
def logged_in():
	if 'username' in session:
		return "logged in as %s" % session['username']
	return 'you are not logged in'

if __name__ == '__main__':
	app.run()