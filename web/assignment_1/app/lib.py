from .view import db
def search_books(query):

	result = db.execute("select * from books where title like :query or isbn like :query or author like :query",
	                    {'query': '%' + query.title() + '%'}).fetchall()
	db.commit()
	return result