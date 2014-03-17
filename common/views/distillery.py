import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from common.models import Distillery, Run, TemperatureDatum, Sensor


def _get_still(still_id):
    try:
        still = Distillery.objects.get(still_id=still_id)
    except Exception as e:
        print("still %s does not exist\n%s" % (still_id, e))
        still = Distillery.objects.get()
    return still


def _get_datum_counts(runs):
    datum_counts = []
    for run in runs:
        count = TemperatureDatum.objects.filter(run=run).count()
        datum_counts.append({"run": run,
                             "count": count})
    return datum_counts


def _get_current_run(runs, run_id):
    if not run_id:
        return runs[0]  # TODO (fix if no runs)
    else:
        return Run.objects.get(run_id=run_id)


def _get_sensor_data_old(still, current_run):
    data_points = TemperatureDatum.objects.filter(run=current_run)
    sensor_values = {}
    for sensor in still.sensors():
        values = data_points.filter(sensor=sensor)
        if values.count() > 0:
            sensor_values[sensor] = values
    shortest = min([sensor_values[sensor].count() for sensor in sensor_values])

    sensor_data = []
    for i in range(0, shortest):
        row = []
        for sensor in sensor_values:
            row.append(sensor_values[sensor][i].value)
        sensor_data.append(row)

    print sensor_data
    return sensor_data


def _get_sensor_data(still, current_run, padding=None):
    data_points = TemperatureDatum.objects.filter(run=current_run)
    max_length = 0
    sensor_values = {}
    for sensor in still.sensors():
        sensor_values[sensor.name] = [datum.value for datum in data_points.filter(sensor=sensor)][:5]
        max_length = max(max_length, len(sensor_values[sensor.name]))

    for sensor_name in sensor_values:
        sensor_values[sensor.name] += [padding] * (max_length - len(sensor_values[sensor.name]))

    return sensor_values, max_length


def distillery(request, still_id, run_id=None):
    still = _get_still(still_id)
    runs = Run.objects.filter(distillery=still)
    current_run = _get_current_run(runs, run_id)
    sensor_data, data_length = _get_sensor_data(still, current_run, 0)
    sensor_ids = [str(sensor.id) for sensor in still.sensors()]

    context = {'still': still,
               'runs': runs,
               'datum_counts': _get_datum_counts(runs),
               'still_id': str(still_id),
               'sensor_ids': sensor_ids,
               'sensor_data': sensor_data,
               'data_length': data_length,
               'data_length_range': range(data_length)
               }
    print json.dumps(context['sensor_data'], sort_keys=True, indent=4, separators=(',', ': '))
    return render_to_response('distillery.html', context)


def distillery_unified(request, still_id):
    still = _get_still(still_id)
    runs = Run.objects.filter(distillery=still)
    current_run = _get_current_run(runs, run_id=None)
    sensor_data, data_length = _get_sensor_data(still, current_run, 0)
    sensor_ids = [str(sensor.id) for sensor in still.sensors()]

    context = {'still': still,
               'still_id': str(still_id),
               'sensor_ids': sensor_ids,
               'sensor_data': sensor_data,
               'data_length': data_length,
               'data_length_range': range(data_length)
               }
    print json.dumps(context['sensor_data'], sort_keys=True, indent=4, separators=(',', ': '))
    return render_to_response('distillery_unified.html', context)


def still_sensor_list(request, still_id=0):
    still = _get_still(still_id)
    return HttpResponse(','.join([sensor.id for sensor in still.sensors()]))
