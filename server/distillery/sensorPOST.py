from flask import jsonify, request
from distillery import app
import databaseHelper as dbHelper

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>/value/<int:sensor_value>", methods=['POST'])
def sensor(still_id, sensor_id, sensor_value):
    return jsonify(dbHelper.addSensorData(still_id,
                                          sensor_id,
                                          sensor_value))
