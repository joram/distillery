from flask import request
from distillery import app

def getSensorData(still_id, sensor_id, seconds_history):
	return -1

def setSensorData(still_id, sensor_id, value):
	return

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>/history/<int:seconds_history>", methods=['GET', 'POST'])
def sensor(still_id, sensor_id, seconds_history):
	if request.method == "GET":
		sensor_val = getSensorData(still_id, sensor_id, seconds_history)
		return "SENSOR:%s is %s" %(sensor_id, sensor_val)
	else:
		sensor_val = request.form['value']
		setSensorData(still_id, sensor_id, sensor_val)
		return "setting SENSOR:%s = %s" %(sensor_id, sensor_val)

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>", methods=['GET', 'POST'])
def sensorDefaultHistory(still_id, sensor_id):
	return sensor(still_id, sensor_id, 100)

# get a list of sensor IDs
@app.route("/still/<int:still_id>/sensors", methods=['GET'])
def sensorList(still_id):
	return "{0,1,2}"
