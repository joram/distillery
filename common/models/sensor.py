from django.db import models
from common.models import TemperatureDatum


class Sensor(models.Model):
    distillery = models.ForeignKey('Distillery')
    sensor_id = models.IntegerField(default=0)
    name = models.CharField(default="", max_length=32)
    colour = models.CharField(default="#FFFFFF", max_length=7)

    @property
    def current_value(self):
        datums = TemperatureDatum.objects.filter().order_by('datetime')
        if datums.count() > 0:
            return datums[0].value
        return -1

    def add_temp_datum(self, value, datetime):
        run = self.distillery.get_run(datum_datetime=datetime)
        TemperatureDatum.objects.create(sensor=self, value=value, datetime=datetime, run=run)

        if run.start_time > datetime:
            run.start_time = datetime
            run.save()

        if run.end_time < datetime:
            run.end_time = datetime
            run.save()

    class Meta:
        unique_together = (("sensor_id", "distillery"),)
        app_label = 'common'
        db_table = 'common_sensor'
        verbose_name_plural = "Sensors"