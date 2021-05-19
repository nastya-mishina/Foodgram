from recipes.models import Ingredient, RecipeIngredient


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            ing_num = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + ing_num]
    return ingredients


def form_valid(form, request, ingredients):
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    for title, count in ingredients.items():
        ingredient, _ = Ingredient.objects.get_or_create(title=title, defaults={'units': 'нет'})
        recipe_ingredient = RecipeIngredient(
            ingredient=ingredient,
            count=count,
            recipe=recipe,
        )
        recipe_ingredient.save()
    form.save_m2m()
