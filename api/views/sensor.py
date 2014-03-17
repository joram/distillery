from django.shortcuts import render_to_response
from common.models import Distillery, Run, TemperatureDatum, Sensor


def get_data(still_id=None, sensor_id=None, run_id=None):

    # collect sensors
    sensors = Sensor.objects.all()
    if still_id:
        still = Distillery.objects.get(still_id=still_id)
        sensors = sensors.filter(still=still)
    if sensor_id:
        sensors = sensors.filter(sensor_id=sensor_id)

    # collect data
    data = []
    for sensor in sensors:
        tempData = TemperatureDatum.objects.filter(sensor=sensor)
        if run_id:
            run = Run.objects.get(run_id=run_id)
            tempData = tempData.filter(run=run)

        if tempData.count() > 0:
            data.append({'sensor': sensor,
                         'data': tempData,
                         })
    return data


def sensor_data(request, still_id=None, sensor_id=None, run_id=None):
    print request.method

    if request.method == "POST":
        print("sensor POST: %s, %s,  %s" % (still_id, sensor_id, run_id))

    if request.method == "GET":
        print("sensor GET: %s, %s,  %s" % (still_id, sensor_id, run_id))
        data = get_data(still_id, sensor_id, run_id)
        return render_to_response("sensor_data.html", {'data': data})
