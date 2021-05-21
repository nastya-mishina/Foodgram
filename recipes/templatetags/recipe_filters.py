import django_filters
from django import template

from recipes.models import Favorite, Follow, Ingredient, ShoppingList

register = template.Library()


@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('tag')


@register.filter(name="get_filter_link")
def get_filter_link(request, tag):
    new_request = request.GET.copy()
    tags = new_request.getlist('tag')

    if tag.style in tags:
        tags.remove(tag.style)
    else:
        tags.append(tag.style)
    new_request.setlist('tag', tags)
    return new_request.urlencode()


class IngredientFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
    )

    class Meta:
        model = Ingredient
        fields = [
            "title",
        ]


@register.filter(name='is_shop')
def is_shop(recipe, user):
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='is_follow')
def is_follow(author, user):
    return Follow.objects.filter(user=user, author=author).exists()
