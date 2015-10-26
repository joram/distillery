from rest_framework import serializers
from common.models import Sensor


class SensorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sensor
        fields = ('distillery', 'sensor_id', 'name', 'colour')
