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

"""
Template Processors
"""
@app.context_processor
def display_year_c():
	from time import strftime
	return dict(show_year="© 2020-" + strftime("%Y"))

@app.context_processor
def inject_user():
	return dict(USERNAME=session.get('username'))

@app.context_processor
def inject_referrer():
	return dict(PREV_URL=request.referrer)

"""
Template filters
"""
@app.template_filter('format_time')
def format_time(s):
	return s.strftime("%x %X")

Session(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
def search():
	if not session.get('user_id'):
		return redirect(url_for('login'))

	if request.method == "POST":
		result=[]
		query = request.form.get("search_string")
		app.logger.info(query)
		if query is not None:
			try:
				query = int(query)
				result = db.execute("select * from books where published_year = :year",{'year':query}).fetchall()
			except ValueError:
				query = '%' + query + '%'
				app.logger.info('titled '+query)
				result = db.execute("select * from books where title ilike :query or isbn like :query or author ilike :query",
			                   {'query':query}).fetchall()
			db.commit()
		return render_template("search.html", books=result)
	elif len(request.args) == 1:
		result=[]
		query = request.args.get('search_string')
		if query is not None:
			query = '%' + query + '%'
			# function(123)
			result = db.execute("select * from books where title ilike :query or isbn ilike :query or author ilike :query",
			                    {'query': query}).fetchall()

		return render_template("search.html",books=result)
	else:
		return render_template('search.html')


@app.route('/book/<isbn>',methods=["GET"])
def book(isbn):
	if not session.get('user_id'):
		return redirect(url_for('login'))
	reviews={}
	data = {}
	if isbn is not None:
		#data = get_reviews(isbn)

		result = db.execute("select * from books where isbn = :isbn", {"isbn": isbn}).fetchone()
		if result is not None:
			gr_avg,gr_ratings = gr_search(isbn, app.config.get('GR_API_KEY'))
			#gr_avg=1;gr_ratings=1
			data = {'isbn': result.isbn, 'title': result.title, 'author': result.author, 'year': result.published_year,
			          'review_count': result.total_reviews,
			          # if the average score is still set at 0.0 then we return 0 as to not get a divide by zero error.
			          'average_score': (result.total_review_score / result.total_reviews) if result.total_reviews > 0 else 0}
			reviews = db.execute("""select reviews.id,reviews.review_score,reviews.review_text,reviews.reviewed_time,users.username
			 from reviews right join users on reviews.user_id = users.id where isbn = :isbn""",
			                     {"isbn": isbn})
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
	app.logger.info(data)
	return render_template('book.html',book_info=data,reviews=reviews)


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
		reviews = None
		if review_id is None and isbns is None:
			return redirect(url_for('search'))
		if review_id is not None:
			#result=db.execute("select * from reviews where id=:id",{'id':id});
			reviews = db.execute("""select reviews.isbn,reviews.review_score,reviews.review_text,reviews.reviewed_time,users.username
			 from reviews right join users on reviews.user_id = users.id where reviews.id = :id""",
			                     {"id": review_id})
		else:
			reviews = db.execute("""select reviews.isbn,reviews.review_score,reviews.review_text,reviews.reviewed_time,users.username from reviews right join users on reviews.user_id = users.id where users.id = :id and reviews.isbn  = :isbn""",{"id": session.get('user_id'),'isbn':isbns}).fetchall()
		if isbns is None:
			abort(500)
		app.logger.info(reviews)
		data = db.execute("select * from books where isbn = :isbn", {"isbn": isbns}).fetchone()
		#db.commit()
		data={**data}

		#data=dict(zip(data.keys(),data))
		data['avg_score'] = 0 if data['total_reviews'] == 0 else round(data['total_review_score']/data['total_reviews'],2)
		if reviews is not None and reviews != []:
			#reviews=dict(zip(reviews.keys(),reviews))
			reviews=dict_proxy(reviews)[0]
			reviews['id']=review_id
		#if result is not None:
		#	result=dict_proxy(result)
		app.logger.info(reviews)
		return render_template('review.html',book_info=data,reviews=reviews)
	if request.method == "POST":
		queried=False
		#update the database with the new fields.
		#db.execute("update books set total_reviews = total_reviews + 1, total_review_score = total_review_score + :review_points;")
		isbn=request.form.get('isbn')
		review_id=request.form.get('id')
		review_text = request.form.get('review_text')
		review_score = request.form.get('review_score')
		username=session.get('username')
		query=''
		if review_id is not None:
			db.execute("""UPDATE books set total_review_score = total_review_score + (select (:review_score-review_score) from reviews where id = :id) where isbn = :isbn""",
			    {'isbn':isbn,'review_score':review_score,'id':review_id})
			result=db.execute("""UPDATE reviews set(review_score,review_text) = (:review_score,:review_text) where id = :id and user_id = :user_id returning reviewed_time""",
				{'id':review_id,'review_score':review_score,'review_text':review_text,'user_id':session.get('user_id')})
			db.commit()
			result=dict_proxy(result)[0]
			reviews={'id':review_id,'username':session.get('username'),'review_score':review_score,'review_text':review_text,'reviewed_time':result['reviewed_time']}
		elif isbn is not None:
			user_id=session.get('user_id')
			rows=db.execute("""select isbn from reviews where user_id = :user_id and isbn = :isbn""",{'user_id':user_id,'isbn':isbn}).fetchone()
			if rows:

				db.execute("""UPDATE books set total_review_score = total_review_score + (select (:review_score-review_score) from reviews where id = :id) where isbn = :isbn""",{'isbn':isbn,'review_score':review_score,'id':review_id})
				
				result = db.execute("""UPDATE reviews set(review_score,review_text) = (:review_score,review_text) where user_id = :user_id and isbn = :isbn RETURNING id,reviewed_time""",
				    {'review_score':review_score,'review_text':review_text,'user_id':user_id,'isbn':isbn})
				#db.session.commit()
			else:
				result =db.execute("""INSERT INTO reviews(review_score,review_text,isbn,user_id) values(:review_score,:review_text,:isbn,:user_id) RETURNING id,reviewed_time;""",
				    {'review_score':review_score,'review_text':review_text,'isbn':isbn,'user_id':user_id})
				
				db.execute("""UPDATE books SET total_reviews = total_reviews + 1, 
				total_review_score = total_review_score + :review_score where isbn=:isbn""",{'review_score':review_score,'isbn':isbn})
				#db.session.commit()
			db.commit()
			result=dict_proxy(result)[0]
			reviews={'id':result['id'],'username':username,'review_score':review_score,'review_text':review_text,'reviewed_time':result['reviewed_time']}
		else:
			reviews=None
		db.commit()
		app.logger.info("Query "+query)
		data = db.execute("select * from books where isbn = :isbn", {"isbn": isbn}).fetchone()
		#db.commit()
		#data=dict_proxy(data)[0]
		data=dict(zip(data.keys(),data))
		data['avg_score'] = 0 if data['total_reviews'] == 0 else round(data['total_review_score']/data['total_reviews'],2)
		app.logger.info(reviews)
		return render_template('review.html',reviews=reviews,book_info=data)
	return redirect(url_for('index'))

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
			gr_avg,gr_ratings = gr_search(isbns, app.config.get('GR_API_KEY'))
			#gr_avg_rating=1
			#gr_total_ratings=1
			data['gr_avg_rating']=gr_avg
			data['gr_total_ratings']=gr_ratings
			result['book']=data;result['reviews']=reviews
			return jsonify(result)

	else:
		return jsonify({'book': False, 'reviews': False})


@app.route('/dashboard')
def dashboard():
	reviews=db.execute("select reviews.*,books.title,books.author from reviews join books on reviews.isbn = books.isbn where user_id = :user_id",{'user_id':session.get('user_id')})
	reviews=dict_proxy(reviews)
	return render_template('dashboard.html',reviews=reviews)

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
		#if data.total_reviews == 0:
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
				return render_template('login.html',msg="The password or username your entered is either incorrect or the user does not exist.")
		else:
			return render_template("login.html", msg="The password or username your entered is either incorrect or the user does not exist.")


@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		pepper = app.config['PEPPER']
		username = request.form.get('username')
		if username is None:
			return render_template('register.html', msg="No username specified")

		if db.execute('select id from users where username=:username', {'username': username}).fetchone() is not None:
			return render_template('register.html', msg="Sorry someone is already registered with that username")
		else:
			password = request.form.get('password')
			password_confirm = request.form.get('password_confirm')

			if password is None :
				return render_template("register.html", msg="No password specified.")
			elif password_confirm is None:
				return render_template("register.html", msg="You didn't specify a verification password.")
			elif password_confirm != password:
				return render_template("register.html", msg="Your verification password didn't match your password.")


			mobile_password = password[0].upper() + password[1:]

			password = auth_tool.hash_password(password, pepper)
			mobile_password = auth_tool.hash_password(mobile_password, pepper)
			db.execute(
				'INSERT INTO USERS(username,password,mobile_password) VALUES (:username,:password,:mobile_password)',
				{'username': username, 'password': password, 'mobile_password': mobile_password})
			db.commit()
			return redirect(url_for("index"))
	else:
		return render_template('register.html')


@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))
	#pass


@app.route('/browse')
def browse():
	books1 = db.execute("SELECT * from books where total_reviews >= 1 order by title").fetchall()
	return render_template('books.html', books=books1)

@app.route('/logged_in')
def logged_in():
	if 'username' in session:
		return "logged in as %s" % session['username']
	return 'you are not logged in'

if __name__ == '__main__':
	app.run()