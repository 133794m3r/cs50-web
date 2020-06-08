import os

from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

credentials=os.getenv("PSQL_CREDS")
engine=create_engine(credentials+'web50')
db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)


@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/books')
def books():
	books=db.execute("SELECT * from books").fetchall()
	return render_template('books.html',books=books)
if __name__ == '__main__':
	app.run()
