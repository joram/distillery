from flask import request
from distillery import app

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>/value/<int:sensor_value>", methods=['POST'])
def sensor(still_id, sensor_id, sensor_value):
	
	return  "SUCCESS %s:%s" % (sensor_id, sensor_value)

