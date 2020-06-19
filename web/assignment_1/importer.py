import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

credentials=os.getenv("PSQL_CREDS")
engine=create_engine(credentials+'web50')
db = scoped_session(sessionmaker(bind=engine))
#It's best practices to open the file like this.
with open("books.csv") as fh:
	#then I read the first line thus-discarding it.
	fh.readline()
	#then I setup the reader based upon the current index of the FH pointer.
	reader=csv.reader(fh)
	#iterate over the list.
	for isbn,title,author,year in reader:
		#if the last check digit is an X put it into the field as a 10 for indexing purposes.
		if isbn[9] == "X":
			isbn_num=(int(isbn[0:9])*100)+10
		else:
			isbn_num=int(isbn)
		#run the actual query. with SQLAlchemy's escaping already included.
		db.execute("INSERT INTO books(isbn,isbn_num,title,author,published_year) values (:isbn,:isbn_num,:title,:author,:year)",
		           {"isbn":isbn,"isbn_num":isbn_num,"title":title,"author":author,"year":year})
		print(f"Added isbn:{isbn} isbn_num:{isbn_num} title:{title} author:{author} year:{year}, to the database.")
db.commit()


