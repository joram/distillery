from datetime import datetime, timedelta
from flask import jsonify, request, url_for
from distillery import app
import database as db
from flask import request, make_response

def any_response(data):
	allowed_origins = ['http://192.168.1.162']
	response = make_response(data)
	origin = request.headers.get('Origin')
	if origin:
		print origin
		response.headers['Access-Control-Allow-Origin'] = origin
	return response

def get_arg(request, key, default=None):
	try:
		value = request.args[key]
	except:
		value = default
	return value

@app.route("/still/<int:still_id>/sensor/<int:sensor_id>",
           methods=['GET'])
@db.check_still
@db.check_sensor
def sensor_history(still_id, sensor_id):
	
	# last known index will default to the most recent
	last_known_index = get_arg(request, 'last_known_index')
	if not last_known_index:
		last_known_index = 0
		sql = "SELECT max(id) FROM sensor_data"
		cur = db.execute(sql)
		rows = cur.fetchall()
		(index,) = rows[0]
		last_known_index = int(index)
		cur.close()

	# previous data wanted
	previous_count = get_arg(request, 'previous_count')
	print previous_count

	# all data after last known index	
	if not previous_count:
		sql = """SELECT time, value, id FROM sensor_data
        	     WHERE still = ? AND sensor = ? AND id > ?
            	 ORDER BY id DESC"""
		handle = db.execute(sql, (still_id, sensor_id, last_known_index))
		rows = handle.fetchall()
		handle.close()
	
	# requested amount of data before last known index
	else:
		sql = """SELECT time, value, id FROM sensor_data WHERE still = ? and sensor = ? and id <= ? ORDER BY id DESC LIMIT ?"""
		handle = db.execute(sql, (still_id, sensor_id, last_known_index, previous_count))
		rows = handle.fetchall()
		handle.close()

	# return the data
	r = jsonify({'count': len(rows),
				 'history': [dict(row) for row in rows] })
	r = any_response(r)
	return r


@app.route("/still/<int:still_id>/sensor/<int:sensor_id>",
           methods=['POST'])
@db.check_sensor
def add_sensor_data(still_id, sensor_id, dtime=datetime.now(), value=None):
	sql = """INSERT INTO sensor_data (still, sensor, time, value) values (?,?,?,?)"""
	if value==None:
		value = request.data
	print "val:%s" % value
	db.execute(sql, (still_id, sensor_id, dtime, value))
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

