import pymysql
from config import DEBUG

db = None
cursor = None

def connect(username, password, database):
	global db, cursor

	db = pymysql.connect("localhost", username, password, database, cursorclass=pymysql.cursors.DictCursor)
	cursor = db.cursor()

def execute(statement):
	global cursor

	cursor.execute(statement)
	return cursor.fetchall()

def commit():
	db.commit()

def disconnect():
	db.close()