from django import forms
from django.forms import CheckboxSelectMultiple

from recipes.models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'time', 'description', 'image')
        widgets = {
            'tags': CheckboxSelectMultiple(
                attrs={'class': 'tags__checkbox'}), }
