from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.utils import json

from recipes.models import Favorite, Follow, Ingredient, Recipe, ShoppingList


@login_required
def favorite_add(request):
    recipe_id = json.loads(request.body)['id']
    recipe = get_object_or_404(Recipe, id=recipe_id)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({'success': True})


@login_required
def favorite_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite_recipe = get_object_or_404(Favorite, user=request.user,
                                        recipe=recipe)
    favorite_recipe.delete()
    return JsonResponse({'success': True})


@login_required
def follow_add(request):
    author_id = json.loads(request.body)['id']
    author = get_object_or_404(User, pk=author_id)
    if request.user != author:
        if Follow.objects.filter(user=request.user).filter(
                author=author).exists() is False:
            Follow.objects.create(user=request.user, author=author)
        return JsonResponse({'success': True})


@login_required
def follow_delete(request, author_id):
    user = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, id=author_id)
    follow = get_object_or_404(Follow, user=user, author=author)
    follow.delete()
    return JsonResponse({'success': True})


@login_required
def shopping_list_add(request):
    recipe_id = json.loads(request.body)['id']
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({'success': True})


@login_required
def shopping_list_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=request.user.username)
    shopping_recipe = get_object_or_404(ShoppingList, user=user, recipe=recipe)
    shopping_recipe.delete()
    return JsonResponse({'success': True})


@login_required
def get_ingredients(request):
    text = request.GET.get('query')
    ingredients = list(Ingredient.objects.filter(
        title__icontains=text).values('title', 'units'))
    return JsonResponse(ingredients, safe=False)
