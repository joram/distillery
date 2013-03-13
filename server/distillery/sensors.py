from datetime import datetime, timedelta
from flask import jsonify, request, url_for
from distillery import app
import database as db


@app.route("/still/<int:still_id>/sensor/<int:sensor_id>",
           methods=['GET'])
def sensor_history(still_id, sensor_id):
    try:
        seconds_history = int(request.args['seconds_history'])
    except (KeyError, TypeError):
        seconds_history = 1000

    sql = """SELECT time, value FROM sensor_data
             WHERE still = ? AND sensor = ? AND time >= ?
             ORDER BY time DESC"""

    time = datetime.now() - timedelta(seconds=seconds_history)
    rows = db.execute(sql, (still_id, sensor_id, time)).fetchall()
    return jsonify(history=[dict(row) for row in rows])


@app.route("/still/<int:still_id>/sensor/<int:sensor_id>",
           methods=['POST'])
@db.check_sensor
def add_sensor_data(still_id, sensor_id):
    dtime = datetime.now()
    sql = """INSERT INTO sensor_data (still, sensor, time, value)
             values (?,?,?,?)"""
    db.execute(sql, (still_id, sensor_id, dtime, request.data))
    db.commit()
    return jsonify({'still':  still_id,
                    'sensor': sensor_id,
                    'time':   dtime.isoformat(),
                    'value':  request.data})


@app.route("/still/<int:still_id>/sensors", methods=['GET'])
@db.check_still
def sensor_list(still_id):
    """ Return array of links to sensors """
    sensors = []

    sql = "SELECT DISTINCT id FROM sensors WHERE still=?"
    for row in db.execute(sql, (still_id,)):
        sensors.append(url_for('sensor_history',
                               still_id=still_id,
                               sensor_id=row[0]))

    return jsonify(sensors=sensors)


@app.route("/debug", methods=['GET'])
def debug():
    rows = [dict(row) for row in db.execute("SELECT * FROM sensor_data")]
    return jsonify(rows=rows)
