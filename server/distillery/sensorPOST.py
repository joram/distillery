from flask import request
from distillery import app
import databaseHelper as dbHelper

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>/value/<int:sensor_value>", methods=['POST'])
def sensor(still_id, sensor_id, sensor_value):
	dbHelper.addSensorData(still_id, sensor_id, sensor_value)
	return  "SUCCESS %s:%s\n%s" % (sensor_id, sensor_value, log)

