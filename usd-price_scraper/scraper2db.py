import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import traceback
import sys
from flask import Flask, render_template, g, send_from_directory, Response
import sqlite3
import argparse

def scrap():
	url = 'https://sp-today.com/en/'
	thepage = requests.get(url)
	urlsoup = BeautifulSoup(thepage.text, "html.parser")

	currency = urlsoup.find(class_='name').text
	value = urlsoup.find(class_="value").text

	print((time.asctime(time.localtime(time.time()))), currency.upper(), value)

	cname = currency.upper()
	DB_NAME = './db-dollar.db'

	try:
		conn = sqlite3.connect(DB_NAME)
		tabel_query = '''CREATE TABLE syp (
									ex_date TEXT NOT NULL,
									currency_name TEXT NOT NULL,
									price REAL NOT NULL);'''

		cursor = conn.cursor()
		print("Successfully Connected to SQLite")
		cursor.execute(tabel_query)
		conn.commit()
		print("SQLite table created")
		cursor.close()

	except sqlite3.Error as error:
		print("Error while creating a sqlite table", error)

	finally:
		if (conn):
			lt = (time.asctime(time.localtime(time.time())))
			cname = currency.upper()
			cur = conn.cursor()
			cur.execute("INSERT INTO syp (ex_date, currency_name, price) VALUES (?,?,?)" ,((time.asctime(time.localtime(time.time()))), cname, value))
			new_id = cur.lastrowid
			conn.commit()
			conn.close()
			print("sqlite connection is closed")

scrap()

app = Flask(__name__)
# app.config["SECRET_KEY"] = "secret!"

DATABASE = './prices.db'
def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db
	
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering or Chrome Frame,
    and also to cache the rendered page for 10 minutes
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r
    
   
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def entrypoint():
    return render_template("index.html")
    
@app.route("/stream")
def stream_page():
	def get_db():
		db = getattr(g, '_database', None)
		if db is None:
			db = g._database = sqlite3.connect(DATABASE)
		return db
	
	cur = get_db().cursor()
	res = cur.execute("select * from syp")
	
	return render_template("/table.html", source=res)


if __name__=="__main__":
    #socketio.run(app,host="0.0.0.0",port="3005",threaded=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port',type=int,default=5000, help="Running port")
    parser.add_argument("-H","--host",type=str,default='0.0.0.0', help="Address to broadcast")
    args = parser.parse_args()
    app.run(host=args.host,port=args.port)

