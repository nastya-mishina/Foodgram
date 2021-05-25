from django.http import JsonResponse

from .models import Ingredient, Ingredients_recipe, ShoppingList


def get_ingredients(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = int(request.POST[
                f'valueIngredient_{_[1]}']
            )
    return ingredients


def get_ingredients_new(request):
    ingredient = request.GET['query']
    ingredients = list(Ingredient.objects.filter(
        title__icontains=ingredient).values('title', 'dimension'))
    return JsonResponse(ingredients, safe=False)


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


def form_valid(form, request, ingredients):
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    for title, units in ingredients.items():
        ingredient, _ = Ingredient.objects.get_or_create(
            title=title, defaults={'dimension': 'нет'})
        recipe_ingredient = Ingredients_recipe(
            ingredient=ingredient,
            units=units,
            recipe=recipe,
        )
        recipe_ingredient.save()
    form.save_m2m()
