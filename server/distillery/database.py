from flask import g
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from distillery import app
import os

def _connect():
    base_directory = os.path.abspath(os.path.dirname(__file__))+"/.."
    db_file = "%s/database.sqlite3" % base_directory
    conn = sqlite3.connect(db_file)
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


def check_still(f):
    """ Function decorator that creates still records as necessary """
    @wraps(f)
    def wrapper(still_id, *args, **kwargs):
        execute("create table if not exists stills(id INT)")
        cursor = execute('SELECT * FROM stills WHERE id=?', (still_id,))
        if not len(cursor.fetchall()):
            execute("INSERT INTO stills (id) values (?)", (still_id,))
            commit()
        return f(still_id, *args, **kwargs)

    return wrapper


def check_sensor(f):
    "Function decorator that creates still and sensor records as necessary"
    @wraps(f)
    def wrapper(still_id, sensor_id, *args, **kwargs):
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
        return f(still_id, sensor_id, *args, **kwargs)

    return check_still(wrapper)
