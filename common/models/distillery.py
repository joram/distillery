from django.db import models
from django.contrib.auth.models import User
from common.models import Run, Sensor
from django.utils.timezone import timedelta, datetime, now as datetime_now


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


class Distillery(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=200)
    still_id = models.IntegerField(unique=True, default=0, primary_key=True)
    last_heartbeat = models.DateTimeField(auto_now=True)

    def get_run(self, datum_datetime, delta_seconds=10):

        # existing run
        for run in Run.objects.filter(distillery=self):
            delta = timedelta(seconds=delta_seconds)
            earliest = run.start_time - delta
            latest = run.end_time + delta
#            print("e:%s \n?:%s \nl:%s\n" % (earliest, datum_datetime, latest))
            if time_in_range(earliest, latest, datum_datetime):
                return run

        # create a new run
        return Run.objects.create(distillery=self,
                                  start_time=datum_datetime,
                                  end_time=datum_datetime)

    @property
    def sensors(self):
        return Sensor.objects.filter(distillery=self)

    @property
    def runs(self):
        return Run.objects.filter(distillery=self)

    def add_temp_datum(self, sensor_id, value, datetime=datetime_now()):
        sensor, _ = Sensor.objects.get_or_create(distillery=self, sensor_id=sensor_id)
        sensor.add_temp_datum(value, datetime)

    @property
    def current_state(self):

        # the no comunication from the server for quite a while
        delta = datetime_now() - self.last_heartbeat
        if delta.total_seconds() > 30:  # TODO: turn into setting
            return 'disconnected'

        return "disconnected"

    def __unicode__(self):
        return u"%s's still: %s" % (self.user, self.name)

    class Meta:
        app_label = 'common'
        db_table = 'common_distillery'
        verbose_name_plural = "Distilleries"