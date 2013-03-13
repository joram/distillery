import sqlite3
import datetime

_db_filename = "database.sqlite3"


def db_cursor():
    db_connection = sqlite3.connect(_db_filename)
    db_cursor = db_connection.cursor()
    return db_cursor


def check_still(still_id):
    cursor = db_cursor()
    cursor.execute("create table if not exists stills(id INT)")
    cursor.execute('SELECT * FROM stills WHERE id==%s' % still_id)
    if len(cursor.fetchall()) <= 0:
        cursor.execute("INSERT INTO stills(id) values (%s)" % still_id)


def check_sensor(still_id, sensor_id):
    check_still(still_id)
    cursor = db_cursor()
    cursor.execute("create table if not exists sensors(still INT, id INT)")
    cursor.execute("""
        create table if not exists sensor_data (
            still INT,
            sensor INT,
            time DATETIME,
            value TEXT(32)
        )
    """)
    cursor.execute('SELECT * FROM sensors WHERE still = ? AND id = ?',
                   (still_id, sensor_id))
    if len(cursor.fetchall()) <= 0:
        cursor.execute("INSERT INTO sensors(still, id) values (?, ?)",
                       (still_id, sensor_id))


def add_sensor_data(still_id, sensor_id, sensor_value):
    check_sensor(still_id, sensor_id)
    cursor = db_cursor()
    dtime = datetime.datetime.now()
    cursor.execute(
        "INSERT INTO sensor_data(still, sensor, time, value) values (?,?,?,?)",
        (still_id, sensor_id, dtime, sensor_value)
    )
