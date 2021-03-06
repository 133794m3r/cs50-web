from .view import db
def dict_proxy(result_proxy):
	#return [{column: value for column, value in rowproxy.items()} for rowproxy in result_proxy]
	return [{**row} for row in result_proxy]

def gr_search(isbn,GR_API_KEY):
	import requests
	result = requests.get("https://www.goodreads.com/book/review_counts.json",params={'key':GR_API_KEY,'isbns':isbn}).json()
	return result['books'][0]['average_rating'],result['books'][0]['ratings_count']

def get_reviews(isbn):
	#book_info = db.execute("select * from books where isbn = :isbn", {'isbn': isbn})
	books_info = db.execute("select * from books where isbn = :isbn",
	                    {'isbn': isbn}).fetchall()
	books_info=dict_proxy(books_info)[0]
	# result=db.execute("select reviews.review_score,reviews.review_text,reviews.reviewed_time,books.isbn,books.title from reviews right join books on reviews.book_id = books.id where reviews.book_id = :book_id",
	#                 {"book_id":book_id}).fetchall()
	reviews = db.execute("""select users.username,reviews.isbn,reviews.review_score,reviews.review_text,reviews.reviewed_time,users.username
	 from reviews right join users on reviews.user_id = users.id where isbn = :isbn""",{"isbn": isbn})
	db.commit()
	result = {}
	if reviews:
		reviews=dict_proxy(reviews)
		# reviews={'query':"select reviews.review_score,reviews.review_text,reviews.reviewed_time,books.isbn,books.title from reviews right join books on reviews.book_id = books.id where reviews.book_id = {}".format(book_id)}
		for i,review in enumerate(reviews):
			ts=reviews[i]['reviewed_time']
			reviews[i]['reviewed_time']=ts.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
		#result['reviews'] = reviews
		#result['book'] = books_info
	else:
		return False

	return reviews