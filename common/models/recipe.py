import json
from django.db import models
from common.models import PumpStep, CollectStep, RecipeRecipeStepMap


class RecipeManager(models.Manager):

    def get_or_create_from_json(self, json_data):
        if type(json_data) == str:
            json_data = json.loads(json_data)

        for recipe in self.all():
            if recipe.to_json(ignore_pump_steps=True) == json_data:
                return recipe, False
        return self.create_from_json(json_data), True

    def create_from_json(self, json_data):
        if type(json_data) == str:
            json_data = json.loads(json_data)

        try:
            recipe = self.create(name=json_data['name'])

            recipe.add_step(PumpStep.objects.create(
                name="fill",
                source="wash",
                destination="boiler"))

            for step_data in json_data['steps']:
                recipe.add_step(CollectStep.objects.create(
                    name=step_data.get("name"),
                    min_temperature=step_data['min'],
                    max_temperature=step_data['max']
                ))
            recipe.add_step(PumpStep.objects.create(
                name="drain",
                source="boiler",
                destination="disposal"))
            return recipe

        except Exception as e:
            print "problem with your json\n%s" % e
            return None


class Recipe(models.Model):
    name = models.CharField(max_length=128)

    objects = RecipeManager()

    def _next_index(self):
        maps = RecipeRecipeStepMap.objects.filter(recipe=self)
        if maps.count() > 0:
            return maps.aggregate(models.Max('step_index'))['step_index__max']
        return 0

    def add_step(self, step):
        return RecipeRecipeStepMap.objects.create(
            recipe_id=self.id,
            recipe_step_id=step.id,
            step_index=self._next_index()
        )

    def steps(self):
        maps = RecipeRecipeStepMap.objects.filter(recipe=self).order_by('step_index')
        return [m.recipe_step for m in maps]

    def to_json(self, ignore_pump_steps=False):
        data = {
            'name': self.name,
            'steps': []}
        for step in self.steps():
            if not ignore_pump_steps or type(step.downcast()) is not PumpStep:
                step = step.downcast()
                data['steps'].append(step.to_json())
        return data

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        app_label = 'common'
        db_table = 'common_recipe'
        verbose_name_plural = "Recipes"
