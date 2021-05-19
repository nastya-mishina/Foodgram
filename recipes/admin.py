from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Tag, Follow, Favorite, ShoppingList


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'units')
    list_filter = ('title',)
    empty_value_display = "-пусто-"


class Ingredients_recipeInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'description', 'time', 'pub_date')
    list_filter = ('title', )
    inlines = (Ingredients_recipeInline, )
    empty_value_display = "-пусто-"


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'style')
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    empty_value_display = "-пусто-"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    empty_value_display = "-пусто-"


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    empty_value_display = "-пусто-"


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Tag, TagAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
