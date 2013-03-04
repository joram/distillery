import os
import sqlite3
from flask import Flask
app = Flask(__name__)


# create the DB if it does not exist
stills = []
stills.append({'name':"John's 2nd still",\
	'sensors':["liquid","lower-steam","upper-steam"], \
	'actuators':["pump-in-mash","pump-in-water","pump-in-boiler","pump-out-boiler","pump-out-garbage"]})

dbFilename = "db.sqlite"
if not os.path.exists(dbFilename):
	conn = sqlite3.connect(dbFilename)
	conn.execute('CREATE TABLE still (name text, id int, creationDatetime datetime)')
	conn.execute('CREATE TABLE sensor (name text, id int, still_id int)')
	conn.execute('CREATE TABLE actuator (name text, id int, still_id int)')
	conn.execute('CREATE TABLE sensorData (still_id int, sensor_id int, value real, loggedDatetime datetime)')
	conn.execute('CREATE TABLE actuatorData (still_id int, actuator_id int, value real, loggedDatetime datetime)')

	for still in stills:
		print("Adding '%s' still" % still['name'])
		# TODO fill in tables: still, sensor, actuator

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

import distillery.sensor
import distillery.actuator
