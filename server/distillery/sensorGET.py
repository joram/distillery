from flask import jsonify, request, url_for
from distillery import app
import database as db


@app.route("/still/<int:still_id>/sensor/<int:sensor_id>",
           methods=['GET'])
def get_sensor(still_id, sensor_id):
    try:
        seconds_history = int(request.args['seconds_history'])
    except (KeyError, TypeError):
        seconds_history = 1000

    history = db.get_sensor_history(still_id,
                                    sensor_id,
                                    seconds_history)
    return jsonify(history=history)


@app.route("/still/<int:still_id>/sensors", methods=['GET'])
def sensor_list(still_id):
    """ Return array of links to sensors """
    sensors = []

    for row in db.get_sensor_list(still_id):
        sensors.append(
            url_for('get_sensor', still_id=still_id, sensor_id=row[0]))

    return jsonify(sensors=sensors)


@app.route("/debug", methods=['GET'])
def debug():
    rows = [dict(row) for row in db.execute("SELECT * FROM sensor_data")]
    return jsonify(rows=rows)
