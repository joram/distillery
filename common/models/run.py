from django.db import models
from common.models import TemperatureDatum


class Run(models.Model):
    run_id = models.AutoField(unique=True, primary_key=True)
    distillery = models.ForeignKey('Distillery')
    start_time = models.DateTimeField('start of this run of the still')
    end_time = models.DateTimeField('end of this run of the still')

    def __unicode__(self):
        return u"still run"

    @classmethod
    def num_data_points(cls):
        print(cls)
        return len(TemperatureDatum.objects.filter(run=cls))

    class Meta:
        app_label = 'common'
        db_table = 'common_run'
        verbose_name_plural = "Runs"
