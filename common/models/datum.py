from django.db import models


class TemperatureDatum(models.Model):
    sensor = models.ForeignKey('Sensor')
    run = models.ForeignKey('Run')
    value = models.FloatField(default=0)
    datetime = models.DateTimeField('date of reading')

    @classmethod
    def sensor_id(cls):
        return cls.sensor.sensor_id

    def celcius(self):
        return self.value

    def __unicode__(self):
        return u"%s" % self.value

    class Meta:
        app_label = 'common'
        db_table = 'common_temperature_datum'