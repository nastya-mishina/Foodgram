from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, ShoppingList


def add_ingredients_to_recipe(recipe, ingredients):
    Recipe.ingredients.through.objects.bulk_create(
        [
            Recipe.ingredients.through(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient,
                    title=ingredient["title"],
                ),
                quantity=ingredient["quantity"],
            )
            for ingredient in ingredients
        ],
    )


def shopping_list_ingredients(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    ingredients = {}
    for item in shopping_list:
        for x in item.recipe.ingredients_recipe_set.all():
            name = f'{x.ingredient.title} ({x.ingredient.dimension})'
            units = x.units
            if name in ingredients.keys():
                ingredients[name] += units
            else:
                ingredients[name] = units
    download = []
    for key, units in ingredients.items():
        download.append(f'{key} - {units} \n')
    return download
