from flask import request
from distillery import app

def getSensorData(still_id, sensor_id):
	return -1

def setSensorData(still_id, sensor_id, value):
	return

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>", methods=['GET', 'POST'])
def sensor(still_id, sensor_id):
	if request.method == "GET":
		sensor_val = getSensorData(still_id, sensor_id)
		return "SENSOR:%s is %s" %(sensor_id, sensor_val)
	else:
		sensor_val = request.form['value']
		setSensorData(still_id, sensor_id, sensor_val)
		return "setting SENSOR:%s = %s" %(sensor_id, sensor_val)
