from django.db import models


class RecipeStep(models.Model):
    name = models.CharField(max_length=128)

    def downcast(self):
        try:
            if self.pumpstep:
                return PumpStep.objects.get(id=self.id)
        except:
            pass

        try:
            if self.collectstep:
                return CollectStep.objects.get(id=self.id)
        except:
            pass


    class Meta:
        app_label = 'common'
        db_table = 'common_recipe_step'
        verbose_name_plural = "RecipeSteps"


class PumpStep(RecipeStep):
    source = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)

    def to_json(self):
        return {
            'name': self.name,
            'src': self.source,
            'dest': self.destination
        }

    def description(self):
        return "%s - %s" % (self.source, self.destination)

    class Meta:
        app_label = 'common'
        db_table = 'common_recipe_pump_step'
        verbose_name_plural = "RecipePumpSteps"


class CollectStep(RecipeStep):
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()

    def to_json(self):
        return {
            'name': self.name,
            'min': self.min_temperature,
            'max': self.max_temperature
        }

    def description(self):
        return "%sC - %sC" % (self.min_temperature, self.max_temperature)

    class Meta:
        app_label = 'common'
        db_table = 'common_recipe_collect_step'
        verbose_name_plural = "RecipeCollectSteps"
