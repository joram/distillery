#!/usr/bin/python
import json
from common.models import Recipe

r = {
    'name': 'the one and only recipe',
    'steps': [
        {
            'name': "methanol",
            'min': 40,
            'max': 78,
        }, {
            'name': "ethanol",
            'min': 78,
            'max': 98,
        }
    ]
}




recipe, created = Recipe.objects.get_or_create_from_json(json.dumps(r))
print "%s %s" % (recipe.id, created)

print json.dumps(recipe.to_json(ignore_pump_steps=True),  sort_keys=True, indent=4, separators=(',', ': '))

#recipe.to_json()
