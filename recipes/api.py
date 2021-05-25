import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Favorite, Follow, Recipe, ShoppingList, User


@login_required
def follow_add(request):
    author_id = json.loads(request.body)["id"]
    author = get_object_or_404(User, pk=author_id)
    if request.user != author:
        if Follow.objects.filter(user=request.user).filter(
                author=author).exists() is False:
            Follow.objects.create(user=request.user, author=author)
            return JsonResponse({"success": "ok"})


@login_required
def follow_delete(request, author_id):
    user = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, id=author_id)
    follow = get_object_or_404(Follow, user=user, author=author)
    follow.delete()
    return JsonResponse({"success": True})


@login_required
def favorite_add(request):
    recipe_id = json.loads(request.body)["id"]
    recipe = get_object_or_404(Recipe, id=recipe_id)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({"success": True})


@login_required
def favorite_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=request.user.username)
    favorite_recipe = get_object_or_404(Favorite, user=user, recipe=recipe)
    favorite_recipe.delete()
    return JsonResponse({"success": True})


@login_required
def shopping_list_add(request):
    recipe_id = json.loads(request.body)["id"]
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({"success": True})


@login_required
def shopping_list_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=request.user.username)
    shopping_list_recipe = get_object_or_404(
        ShoppingList,
        user=user,
        recipe=recipe,
    )
    shopping_list_recipe.delete()
    return JsonResponse({"success": True})
