from django.contrib import admin

from .models import (Favorite, Ingredient, Purchase, Recipe, RecipeIngredient,
                     Tag)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    search_fields = ('title',)


class RecipeAdmin(admin.ModelAdmin):
    def count_favorites(self, obj):
        return obj.in_favorites.count()

    count_favorites.short_description = 'favorites'

    list_display = ('pk', 'title', 'author', 'count_favorites')
    exclude = ('tags',)
    search_fields = ('title', 'author__username')
    list_filter = ('pub_date',)
    inlines = (IngredientInline, TagInline)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'quantity')


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'color')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
