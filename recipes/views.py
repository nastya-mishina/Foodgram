from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .constants import ELEMENTS_PAGE
from .forms import RecipeForm
from .models import (
    Follow,
    Ingredients_recipe,
    Recipe,
    ShoppingList,
    User,
)
from .utils import form_valid, get_ingredients, shopping_list_ingredients


def index(request):
    tags = request.GET.getlist('filters')
    recipe = Recipe.objects.all()
    if tags:
        recipe = recipe.filter(tags__style__in=tags).distinct().all()
    paginator = Paginator(recipe, ELEMENTS_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        ingredients = get_ingredients(request)
        if form.is_valid():
            form_valid(form, request, ingredients)
            return redirect('index')
    return render(request, "recipe_new.html", {"form": form})


def profile(request, username):
    tags = request.GET.getlist('filters')
    recipe = Recipe.objects.filter(author__username=username).all()
    if tags:
        recipe = recipe.filter(tags__style__in=tags).distinct().all()
    author = get_object_or_404(User, username=username)
    paginator = Paginator(recipe, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page': page, 'author': author})


def recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, username=username)
    return render(request, 'recipe.html', {'recipe': recipe, 'author': author})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )
    if request.method == 'POST':
        ingredients = get_ingredients(request)
        if form.is_valid():
            Ingredients_recipe.objects.filter(recipe=recipe).delete()
            form_valid(form, request, ingredients)
            return redirect('index')
    return render(
        request,
        "recipe_edit.html",
        {"form": form, 'recipe': recipe},
    )


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect('index')


@login_required
def follow(request):
    recipes_author = Follow.objects.filter(user=request.user)
    paginator = Paginator(recipes_author, ELEMENTS_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page})


@login_required
def favorite(request):
    tags = request.GET.getlist('filters')
    recipes_favorite = Recipe.objects.filter(
        favorite_recipe__user__id=request.user.id).all()
    if tags:
        recipes_favorite = recipes_favorite.filter(
            tags__style__in=tags).distinct().all()
    paginator = Paginator(recipes_favorite, ELEMENTS_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html', {'page': page})


@login_required
def shopping_list(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    return render(
        request,
        'shopping_list.html',
        {'shopping_list': shopping_list},
    )


@login_required
def shopping_list_download(request):
    result = shopping_list_ingredients(request)
    response = HttpResponse(result, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename = download.txt'
    return response


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
