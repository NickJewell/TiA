from flask import render_template
from app import app
from itertools import izip
import sqlite3 as lite

DATABASE = '/Users/nick/TiA/test.db'

def get_db():
    db = lite.connect(DATABASE)
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
@app.route('/nick')
def nick():
	
	
	
	rec = query_db('select * from Results order by Imp Desc')
	

	#for record in cur.fetchall():
	#	x = [dict(imp=record[5], user=record[2], url=record[1], highlights=record[7])]
	#	print x[imp]
		#print "Importance: %.2f\t%s"%(record[5], record[2])
		#print "URL: %s"%(record[1])
		#print "Highlights:\n%s\n\n"%(record[7])
	
	#user = { 'nickname': 'Joseph' }
	#posts = [
	#	{ 
	#		'author': { 'nickname': 'Charlotte' }, 
	#		'body': 'Rumble rumble rumble!' 
	#	},
	#	{ 
	#		'author': { 'nickname': 'Lottie' }, 
	#		'body': 'Ka-Ching!' 
	#	}
	#	]
	return render_template("nick.html",
		records = rec)



