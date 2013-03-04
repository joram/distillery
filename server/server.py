#!/usr/bin/python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/still/<int:still_id>")
def still(still_id):
	return "GET STILL:%s" %still_id

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>")
def sensor(still_id,sensor_id):
	return "GET STILL:%s, SENSOR:%s" %(still_id,sensor_id)

@app.route("/still/<int:still_id>/actuator/<int:actuator_id>")
def sensor(still_id,actuator_id):
	return "GET STILL:%s, ACTUATOR:%s" %(still_id,actuator_id)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
