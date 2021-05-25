from django.db.models import Sum
from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, RecipeIngredient


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


def shopping_list_ingredients(request_user):
    ingredients = (
        RecipeIngredient.objects.filter(
            recipe__in_purchases__user=request_user,
        ).values(
            "ingredient__title",
            "ingredient__dimension",
        ).annotate(quantity=Sum("quantity"))
    )
    download_list = []
    for ingredient in ingredients:
        download_list.append(
            f'{ingredient["ingredient__title"]} '
            f'{ingredient["quantity"]} '
            f'{ingredient["ingredient__dimension"]} \n')
    return download_list
