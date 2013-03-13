from flask import request
from distillery import app

class datum():
	def __init__(self, dt, temp, name="datum"):
		self.name = name
		self.datetime = dt
		self.temperature = temp
	def __str__(self):
		return '"%s":{ "datetime":"%s", "temperature":"%s" }' % (self.name, self.datetime, self.temperature)


class sensorData():
	def __init__(self, name, rawData):
		self.name = name
		self.data = []
		for (name,val) in rawData:
			self.data.append(datum(name,val))
	def __str__(self):
		datumStrings = []
		for datum in self.data:
			datumStrings.append(str(datum))
		return ',\n'.join(datumStrings)	
	

def getSensorData(still_id, sensor_id, seconds_history):
	return -1

def setSensorData(still_id, sensor_id, value):
	return

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>/history/<int:seconds_history>", methods=['GET'])
@app.route("/still/<int:still_id>/sensor/<int:sensor_id>", methods=['GET'])
def sensor(still_id, sensor_id, seconds_history=100):
	sensor_val = getSensorData(still_id, sensor_id, seconds_history)

	returnedData = []
	returnedData.append(("sensor1",[("time1","value1"),("time2","value2")]))	
	returnedData.append(("sensor2",[("time3","value3"),("time4","value4")]))	

	sensorStrings = []
	for (name, data) in returnedData:
		sensorStrings.append( str(sensorData(name, data)) )
	return  "{\n%s\n}"  % ',\n'.join(sensorStrings)	

# get a list of sensor IDs
@app.route("/still/<int:still_id>/sensors", methods=['GET'])
def sensorList(still_id):
	return "{0,1,2}"
