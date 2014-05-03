from django.db import models
from common.models import TemperatureDatum


class Run(models.Model):
    run_id = models.AutoField(unique=True, primary_key=True)
    distillery = models.ForeignKey('Distillery')
    recipe = models.ForeignKey('Recipe', null=True)
    start_time = models.DateTimeField('start of this run of the still')
    end_time = models.DateTimeField('end of this run of the still')

    def __unicode__(self):
        return u"still run"

    @property
    def num_data_points(cls):
        return len(TemperatureDatum.objects.filter(run=cls))

    @property
    def time_elapsed_seconds(self):
        return (self.end_time - self.start_time).total_seconds()

    class Meta:
        app_label = 'common'
        db_table = 'common_run'
        verbose_name_plural = "Runs"
