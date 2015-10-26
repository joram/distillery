from datetime import datetime

from common.models import Distillery, Run, TemperatureDatum, Sensor
from django.http import HttpResponse

DEFAULT_NUM_ROWS = 10





def recent_data(request, still_id, sensor_id):
    num_rows = request.GET.get('num_rows', DEFAULT_NUM_ROWS)
    still = Distillery.objects.get(still_id=still_id)
    sensor = Sensor.objects.get(distillery=still, id=sensor_id)
    data = TemperatureDatum.objects.filter(sensor=sensor).order_by('datetime')[:num_rows]
    values = ["%s, %s" % (datum.datetime, datum.value) for datum in data if datum.value]
    sensor_name = sensor.name if sensor.name else "sensor_%s" % sensor_id
    return HttpResponse("time, %s\n%s" % (sensor_name, "\n".join(values)))


# TODO IN THE _line_graph, do time better:
#  https://developers.google.com/chart/interactive/docs/gallery/annotatedtimeline?csw=1
def recent_data_all_sensors(request, still_id):
    num_rows = request.GET.get('num_rows', DEFAULT_NUM_ROWS)
    try:
        num_rows = int(num_rows)
    except ValueError:
        print "someone passed a bad GET PARAM: '%s' should be an int" % request.GET.get('num_rows')
        num_rows = DEFAULT_NUM_ROWS

    still = Distillery.objects.get(still_id=still_id)
    sensors = Sensor.objects.filter(distillery=still)

    if len(sensors) == 0:
        return HttpResponse()

    # first column (time)
    datums = TemperatureDatum.objects.filter(sensor=sensors[0]).order_by('datetime')[:num_rows]
    result_data = [[datum.datetime.strftime("%H:%M:%S")] for datum in datums]

    # temp columns (C)
    for sensor in sensors:
        datums = TemperatureDatum.objects.filter(sensor=sensor).order_by('datetime')[:num_rows]
        temperatures = []

        # pad with blanks if we're missing data
        if datums.count() < num_rows:
            temperatures = ['0'] * (num_rows-datums.count())

        temperatures.extend(['%s' % datum.celcius() for datum in datums])

        for x in range(0, len(result_data)):
            result_data[x].extend([temperatures[x]])

    # first rows (titles)
    result_titles = ["time"]
    result_titles.extend([sensor.get_name for sensor in sensors])
    data = [result_titles]
    data.extend(result_data)

    response_str = "\n".join([", ".join(row) for row in data])
    return HttpResponse(response_str)
