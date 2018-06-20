#!/usr/bin/python
from datetime import datetime, timedelta
from common.models import Distillery, Sensor, TemperatureDatum, Run

STILL_NAME = 'bertha'

still, _ = Distillery.objects.get_or_create(name=STILL_NAME)

sensors = [
 {'name': "boiler",
  'colour': "#FFFFFF",
  "id": 0},
 {'name': "external",
  'colour': "#FFFFFF",
  "id": 1},
 {'name': "collection",
  'colour': "#FFFFFF",
  "id": 2},
]
for s in sensors:
    sensor, _ = Sensor.objects.get_or_create(
        distillery=still,
        name=s['name'],
        sensor_id=s['id'],
        colour=s['colour'])
    run, _ = Run.objects.get_or_create(
        distillery=still,
        start_time=datetime.now(),
        end_time=datetime.now())
    for i in range(0, 100):
        TemperatureDatum.objects.create(
            sensor=sensor,
            run=run,
            value=20*sensors.index(s),
            datetime=datetime.now() - timedelta(minutes=i))
