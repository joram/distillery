from rest_framework import viewsets

from common.models import Distillery
from common.serializers import DistillerySerializer


class DistilleryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Distillery.objects.all()
    serializer_class = DistillerySerializer
