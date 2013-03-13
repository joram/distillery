from flask import g
import sqlite3
from datetime import datetime, timedelta

from distillery import app


def _connect():
    conn = sqlite3.connect("database.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn


def get_connection():
    """
    Return the request-context database connection or get a new one.
    """
    return getattr(g, 'db', False) or _connect()


@app.before_request
def connect_database():
    g.db = get_connection()


@app.teardown_request
def close_database(exc):
    if hasattr(g, 'db'):
        g.db.close()


def execute(*args):
    return get_connection().execute(*args)


def commit():
    return get_connection().commit()


def check_still(still_id):
    execute("create table if not exists stills(id INT)")
    cursor = execute('SELECT * FROM stills WHERE id=?', (still_id,))
    if not len(cursor.fetchall()):
        execute("INSERT INTO stills (id) values (?)", (still_id,))
        commit()


def check_sensor(still_id, sensor_id):
    check_still(still_id)
    execute("create table if not exists sensors(still INT, id INT)")
    execute("""
        create table if not exists sensor_data (
            still INT,
            sensor INT,
            time DATETIME,
            value TEXT(32)
        )
    """)
    res = execute('SELECT * FROM sensors WHERE still = ? AND id = ?',
                  (still_id, sensor_id))
    if not len(res.fetchall()):
        execute("INSERT INTO sensors(still, id) values (?, ?)",
                (still_id, sensor_id))
        commit()


def add_sensor_data(still_id, sensor_id, sensor_value):
    check_sensor(still_id, sensor_id)
    dtime = datetime.now()
    sql = """INSERT INTO sensor_data (still, sensor, time, value)
             values (?,?,?,?)"""
    execute(sql, (still_id, sensor_id, dtime, sensor_value))
    commit()
    return {'still':  still_id,
            'sensor': sensor_id,
            'time':   dtime.isoformat(),
            'value':  sensor_value}


def get_sensor_history(still, sensor, seconds_history):
    check_sensor(still, sensor)
    sql = """SELECT time, value FROM sensor_data
             WHERE still = ? AND sensor = ? AND time >= ?
             ORDER BY time DESC"""
    time = datetime.now() - timedelta(seconds=seconds_history)
    rows = execute(sql, (still, sensor, time)).fetchall()

    return [dict(row) for row in rows]


def get_sensor_list(still):
    return execute("SELECT id FROM sensors WHERE still=?", (still,))
