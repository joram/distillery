#!/usr/bin/python
from common.models import Distillery, Sensor

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
for sensor in sensors:
    Sensor.objects.get_or_create(distillery=still,
                                 name=sensor['name'],
                                 id=sensor['id'],
                                 colour=sensor['colour'])
