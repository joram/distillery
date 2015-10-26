from django.shortcuts import render_to_response

from rest_framework import viewsets

from common.models import Distillery, Run, TemperatureDatum, Sensor
from common.serializers import SensorSerializer


class SensorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


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

    if request.method == "GET":
        data = get_data(still_id, sensor_id, run_id)
        return render_to_response("sensor_data.html", {'data': data})
