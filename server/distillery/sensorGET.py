from flask import jsonify, url_for
from distillery import app
import database as db


def get_sensor_data(still_id, sensor_id, seconds_history):
    return -1


@app.route("/still/<int:still_id>/sensor/<int:sensor_id>/history/<int:seconds_history>", methods=['GET'])
@app.route("/still/<int:still_id>/sensor/<int:sensor_id>", methods=['GET'])
def sensor(still_id, sensor_id, seconds_history=100):
    #sensor_val = get_sensor_data(still_id, sensor_id, seconds_history)

    returned_data = {}
    returned_data["sensor1"] = [("time1", "value1"), ("time2", "value2")]
    returned_data["sensor2"] = [("time3", "value3"), ("time4", "value4")]

    return jsonify(returned_data)


@app.route("/still/<int:still_id>/sensors", methods=['GET'])
def sensor_list(still_id):
    """ Return array of links to sensors """
    sensors = []

    for sensor_id in [0, 1, 2]:
        sensors.append(
            url_for('sensor', still_id=still_id, sensor_id=sensor_id))

    return jsonify(sensors)


@app.route("/debug", methods=['GET'])
def debug():
    cur = db.db_cursor()
    cur.execute("SELECT * FROM sensor_data")
    return jsonify(cur.fetchall())
