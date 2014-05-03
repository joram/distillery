from django.db import models


class RecipeRecipeStepMap(models.Model):
    step_index = models.IntegerField()
    recipe = models.ForeignKey('Recipe')
    recipe_step = models.ForeignKey('RecipeStep')

    class Meta:
        app_label = 'common'
        db_table = 'common_recipe_recipe_step_map'
        verbose_name_plural = "RecipeRecipeStepMaps"

