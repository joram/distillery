from distillery import app, database, sensors
import datetime
import math
        

def fillData(still_id, sensor_id, func, stime, etime):
    readingDelta = datetime.timedelta(seconds=5)
    dtime = stime
    with app.test_request_context():
        app.preprocess_request()
        while dtime <= etime:
            sensors.add_sensor_data(still_id, sensor_id, dtime, func(dtime))
            dtime += readingDelta

endTime = datetime.datetime.now()
startTime = endTime - datetime.timedelta(hours=1)
still_id = 1

def horizontal(t):
    return 50

def incremental(t):
    ratio = (startTime-t).total_seconds()/(startTime-endTime).total_seconds()
    return 20+80*(ratio)

def sinusoidal(t):
    i = (datetime.datetime.now() - t).total_seconds()
    return math.sin(i)*50+50

print "loading horizontal line data"
fillData(1, 0, horizontal, startTime, endTime)
print "loading incremental line data"
fillData(1, 1, incremental, startTime, endTime)
print "loading sinusoidal line data"
fillData(1, 2, sinusoidal, startTime, endTime)

