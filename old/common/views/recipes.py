from django.shortcuts import render_to_response
from common.models.recipe import Recipe


def recipes(request):
    recipes = []
    for recipe in Recipe.objects.all():
        steps = []
        for step in recipe.steps():
            steps.append({
                'name': step.name,
                'details': step.downcast().description()
            })
        recipes.append({
            'name': recipe.name,
            'steps': steps
        })

    recipes.append(recipes[0])
    recipes.append(recipes[0])
    recipes.append(recipes[0])
    recipes.append(recipes[0])
    recipes.append(recipes[0])

    context = {
        'page': 'recipes',
        'recipes': recipes}
    return render_to_response('recipes/recipes.html', context)

