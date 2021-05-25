from django.forms import CheckboxSelectMultiple, ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'cooking_time', 'text', 'image']
        widgets = {'tags': CheckboxSelectMultiple()}
