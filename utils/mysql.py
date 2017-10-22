import pymysql
import env

db = None
cursor = None

def isAlive():
	if db == None:
		return False

	return db.open

def create():
	global db, cursor

	db = pymysql.connect("localhost", 'glacibot', env.SQLPASS, 'glacibot', cursorclass=pymysql.cursors.DictCursor)
	cursor = db.cursor()

def execute(statement):
	global cursor

	cursor.execute(statement)
	return cursor.fetchall()

def commit():
	db.commit()

def escape(text):
	return db.escape(text)

def destroy():
	db.close()