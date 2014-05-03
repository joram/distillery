import json
from django import template
from common.models import Run
from django.shortcuts import render_to_response
from common.models import Distillery, TemperatureDatum
from django.db.models import Max

register = template.Library()


def _get_current_run(runs, run_id):
    if not run_id:
        return runs[0]  # TODO (fix if no runs)
    else:
        return Run.objects.get(run_id=run_id)


def _get_sensor_data(still, current_run, padding=None):
    data_points = TemperatureDatum.objects.filter(run=current_run)
    max_length = 0
    sensor_values = {}
    for sensor in still.sensors:
        sensor_values[sensor.name] = [datum.value for datum in data_points.filter(sensor=sensor)][:5]
        max_length = max(max_length, len(sensor_values[sensor.name]))

    for sensor_name in sensor_values:
        sensor_values[sensor.name] += [padding] * (max_length - len(sensor_values[sensor.name]))

    return sensor_values, max_length


@register.simple_tag
def unified_sensor_graph(still_id):
    still, created = Distillery.objects.get_or_create(still_id=still_id)
    runs = Run.objects.filter(distillery=still)
    max_run_id = runs.aggregate(Max('run_id')).get('run_id__max')
    current_run = runs.get(run_id=max_run_id) if max_run_id else None

    sensor_data, data_length = _get_sensor_data(still, current_run, 0)
    sensor_ids = [str(sensor.id) for sensor in still.sensors]

    context = {'still': still,
               'sensor_ids': sensor_ids,
               'sensor_data': sensor_data,
               'UUID': "_%s" % still_id,
               'data_URI': "/ajax/still/%s/allsensors/?num_rows=50" % still_id,
               'data_length': data_length,
               'data_length_range': range(data_length)
               }

    #print json.dumps(context['sensor_data'], sort_keys=True, indent=4, separators=(',', ': '))
    return render_to_response('graphs/distillery_unified.html', context)
