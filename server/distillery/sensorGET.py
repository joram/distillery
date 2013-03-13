from flask import jsonify, url_for
from distillery import app
import databaseHelper as dbHelper


def getSensorData(still_id, sensor_id, seconds_history):
    return -1

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>/history/<int:seconds_history>", methods=['GET'])
@app.route("/still/<int:still_id>/sensor/<int:sensor_id>", methods=['GET'])
def sensor(still_id, sensor_id, seconds_history=100):
    sensor_val = getSensorData(still_id, sensor_id, seconds_history)

    returnedData = {}
    returnedData["sensor1"] = [("time1","value1"),("time2","value2")]
    returnedData["sensor2"] = [("time3","value3"),("time4","value4")]

    return jsonify(returnedData)

# get a list of sensor IDs
@app.route("/still/<int:still_id>/sensors", methods=['GET'])
def sensorList(still_id):
    sensors = []

    for sensor_id in [0, 1, 2]:
        sensors.append(
            url_for('sensor', still_id=still_id, sensor_id=sensor_id))

    return jsonify(sensors)

@app.route("/debug", methods=['GET'])
def debug():
    cur = dbHelper.dbCursor()
    cur.execute("SELECT * FROM sensorData")
    return jsonify(cur.fetchall())
