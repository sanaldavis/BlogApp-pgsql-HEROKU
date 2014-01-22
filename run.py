from flask import *
from time import *
import psycopg2
import os
import urlparse
import database

app=Flask(__name__)
app.secret_key = 'sanu'

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])


@app.route('/')
def welcome():
	return render_template('home.html')

@app.route('/home')
def home():
	#con=lite.connect(database='chackobhavan')
	
	con = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
        cur=con.cursor()
        cur.execute("SELECT * FROM blog_database ORDER BY id desc")
	post = [ dict ( id = i[0], author = i[1], post = i[2], day = i[3], time = i[4] ) for i in cur.fetchall() ]
        con.commit()
        con.close()
	if 'logged_in' in session:
		return render_template('home_logout.html', post = post)
	else:
		return render_template('home.html', post = post)

@app.route('/post')
def post():
	if 'logged_in' in session:
		return render_template('post.html')
	else:
		return redirect(url_for('login'))

@app.route('/post', methods=['POST'])
def post_store():
	#con=lite.connect(database = 'chackobhavan')
	
	con = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)

	cur=con.cursor()
	cur.execute("INSERT INTO blog_database(author, post, day, time) VALUES(%s,%s,%s,%s)", [ request.form['name'], request.form['blogpost'], strftime( "%d %b %Y" , gmtime()), strftime( "%H:%M:%S", gmtime())]) 
	con.commit()
	con.close()
	return render_template('post.html')

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] == 'sanal' and request.form['password'] == 'tharayil':
			session['logged_in'] = True
			return redirect(url_for('post'))
		else:
			error = 'Please check username and password'

	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None )
	return redirect(url_for('login'))

#app.run(debug = True)
if __name__ == "__main__":
    	port = int(os.environ.get("PORT", 5000))
    	app.run(host='0.0.0.0', port=port)

