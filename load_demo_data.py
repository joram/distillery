from distillery import app, database, sensors
import datetime
import math
 
still_id = 1       
sensors.add_sensor_data(still_id, 0, datetime.datetime.now(), 20)
sensors.add_sensor_data(still_id, 1, datetime.now(), 20)
sensors.add_sensor_data(still_id, 2, datetime.now(), 20)


