from flask import jsonify, request
from distillery import app
import database as db

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>",
           methods=['POST'])
def sensor(still_id, sensor_id):
    return jsonify(db.add_sensor_data(still_id,
                                      sensor_id,
                                      request.data))
