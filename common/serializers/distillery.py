from rest_framework import serializers
from common.models import Distillery


class DistillerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Distillery
        fields = ('user', 'name', 'still_id', 'last_heartbeat')
