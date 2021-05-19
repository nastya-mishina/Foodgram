from django.db.models import Sum
from django.http import HttpResponse

from .models import Recipe, Ingredient, User, Follow, ShoppingList, Favorite, Tag, RecipeIngredient
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from .utils import get_ingredients, form_valid


def index(request):
    recipe_list = Recipe.objects.all()
    tags = request.GET.getlist('tag')
    if tags:
        recipe_list = recipe_list.filter(tags__style__in=tags).distinct().all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator})


@login_required
def new_recipe(request):
    if request.method != "POST":
        form = RecipeForm()
        return render(request, 'new_recipe.html', {'form': form})
    form = RecipeForm(request.POST, files=request.FILES)
    ingredients = get_ingredients(request)
    if form.is_valid():
        form_valid(form, request, ingredients)
        return redirect('index')
    return render(request, 'new_recipe.html', {'form': form})


def profile(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    follow = author.following.filter(user=user.id).exists()
    following = author.following.count()
    follower = author.follower.count()
    recipes = author.recipes.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'profile.html', {'paginator': paginator,
                                            'page': page, 'author': author, 'following': following,
                                            'follow': follow, 'follower': follower})


def recipe_view(request, username: str, recipe_id: int):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    author = recipe.author
    follow = author.following.filter(user=user.id).exists()
    following = author.following.count()
    follower = author.follower.count()
    form = RecipeForm()
    ingredients = recipe.ingredients.all()
    count_recipes = author.recipes.count
    return render(request, 'recipe_one.html', {'recipe': recipe, 'author': author,
                                               'follow': follow, 'following': following, 'follower': follower,
                                               'form': form, 'ingredients': ingredients,
                                               'count_recipes': count_recipes})


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )
    if request.method == 'POST':
        ingredients = get_ingredients(request)
        if form.is_valid():
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            form_valid(form, request, ingredients)
            return redirect('index')
    return render(
        request,
        "recipe_edit.html",
        {"form": form, 'recipe': recipe},
    )


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect('index')


@login_required
def follow_index(request):
    follows = Follow.objects.filter(user=request.user)
    paginator = Paginator(follows, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {'page': page})


@login_required
def shopping_list(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    return render(
        request,
        'shopList.html',
        {'shopping_list': shopping_list})


@login_required
def download_shopping_list(request):
    ingredients = Recipe.objects.prefetch_related('ingredients', 'recipe_ingredients').filter(
        recipe_shopping_list__user=request.user).order_by('ingredients__title').values(
        'ingredients__title', 'ingredients__units').annotate(
        count=Sum('recipe_ingredients__count'))
    ingredient_txt = [
        (f"\u2022 {item['ingredients__title'].capitalize()} "
         f"({item['ingredients__units']}) \u2014 {item['count']} \n")
        for item in ingredients
    ]
    filename = 'shoplist.txt'
    response = HttpResponse(ingredient_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@login_required
def favorite(request):
    recipes = Recipe.objects.filter(
        recipe_favorite_list__user__id=request.user.id).all()
    tags = request.GET.getlist('tag')
    if tags:
        recipes = recipes.filter(tags__style__in=tags).distinct().all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html', {'paginator': paginator, 'page': page, })


def page_not_found(request):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
