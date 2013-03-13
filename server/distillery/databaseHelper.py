import sqlite3
import datetime
_db_filename = "database.sqlite3"

def dbCursor():
	dbConnection = sqlite3.connect(_db_filename)
	dbCursor = dbConnection.cursor()
	return dbCursor	


def checkStill(still_id):
	cursor = dbCursor()
	cursor.execute("create table if not exists stills(id INT)")
	cursor.execute('SELECT * FROM stills WHERE id==%s' % still_id)
	if len(cursor.fetchall())<=0:
		cursor.execute("INSERT INTO stills(id) values (%s)" % still_id)


def checkSensor(still_id, sensor_id):
	checkStill(still_id)
	cursor = dbCursor()
	cursor.execute("create table if not exists sensors(still INT, id INT)")
	cursor.execute("create table if not exists sensorData(still INT, sensor INT, time DATETIME, value TEXT(32))")
	cursor.execute('SELECT * FROM sensors WHERE still==%s AND id==%s' % (still_id,sensor_id))
	if len(cursor.fetchall() )<=0:
		cursor.execute("INSERT INTO sensors(still, id) values (%s, %s)" % (still_id, sensor_id))
	
	
def addSensorData(still_id, sensor_id, sensor_value):
	checkSensor(still_id, sensor_id)
	cursor = dbCursor()
	dtime = datetime.datetime.now()
	cursor.execute("INSERT INTO sensorData(still, sensor, time, value) values (?,?,?,?)" % (still_id, sensor_id, dtime, sensor_value))

