#import psycopg2 as lite
import os
import psycopg2
import urlparse
con=None
#con=lite.connect(database='chackobhavan')
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

con = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
cur=con.cursor()
cur.execute('''CREATE TABLE blog_database( id serial, author text, post text, day text, time text, comment text)''')
con.commit()
con.close()

