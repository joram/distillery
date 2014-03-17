#!/usr/bin/python
from common.models import Distillery
import os
import sqlite3
from dateutil import parser
import datetime
import pytz

#dbs =  ["old_data.sqlite3", "old_data_2.sqlite3"]
dbs = ["old_data_2.sqlite3"]

SCRIPT_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
for old_db_file in dbs:
    full_db_path = os.path.join(SCRIPT_BASE_DIR, old_db_file)
    print(full_db_path)
    con = sqlite3.connect(full_db_path)
    #cur = con.cursor()

    dt_conversion = {}
    for row in con.execute("SELECT still,  sensor, time, value, id FROM sensor_data"):
        # still,  sensor, time, value id
        (still_id, sensor_id, dtime, value, row_id) = row

        # adjust times
        dtime = pytz.utc.localize(parser.parse(dtime))
        if sensor_id not in dt_conversion:
            dt_conversion[sensor_id] = {}

        if dtime in dt_conversion[sensor_id]:
            dt_conversion[sensor_id][dtime] += datetime.timedelta(seconds=3)
            dtime = dt_conversion[sensor_id][dtime]
        else:
            dt_conversion[sensor_id][dtime] = dtime

        print("%s: %s-%s=%s" % (dtime, still_id, sensor_id, value))

        still, _ = Distillery.objects.get_or_create(still_id=still_id)
        still.add_temp_datum(sensor_id=sensor_id, value=value, datetime=dtime)