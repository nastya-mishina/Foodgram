import io
import os

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from .models import Ingredient, Recipe, RecipeIngredient

X_COORDINATE = 50
Y_COORDINATE_TITLE = 50
FONT_SIZE = 18
Y_COORDINATE_TEXT = 130
SIZE_DOWN_TITLE = 25
SIZE_DOWN_TEXT = 44
FONT_SIZE_TEXT = 12
FONT = "GOST_Common"


def add_ingredients_to_recipe(recipe, ingredients):
    Recipe.ingredients.through.objects.bulk_create(
        [
            Recipe.ingredients.through(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient,
                    title=ingredient["title"],
                ),
                quantity=ingredient["quantity"],
            )
            for ingredient in ingredients
        ],
    )


pdfmetrics.registerFont(
    TTFont(
        "GOST_Common",
        os.path.join("font/GOST_Common.ttf"),
    )
)


def generate_pdf(user):
    buffer = io.BytesIO()
    canvas = Canvas(buffer, bottomup=0)

    title = "Список покупок"
    canvas.setTitle(title)

    canvas.setFont(FONT, FONT_SIZE)
    canvas.drawString(X_COORDINATE, Y_COORDINATE_TITLE, title)

    canvas.setFont(FONT, FONT_SIZE)
    canvas.drawString(
        X_COORDINATE, Y_COORDINATE_TITLE + SIZE_DOWN_TITLE, "Продукты:"
    )
    y_coordinate = 130
    canvas.setFont(FONT, FONT_SIZE_TEXT)

    ingredients = (
        RecipeIngredient.objects.filter(
            recipe__in_purchases__user=user,
        )
        .values(
            "ingredient__title",
            "ingredient__dimension",
        )
        .annotate(quantity=Sum("quantity"))
    )
    for ingredient in ingredients:
        line = "{0} {1} {2}".format(
            ingredient["ingredient__title"],
            ingredient["quantity"],
            ingredient["ingredient__dimension"],
        )
        canvas.drawString(X_COORDINATE, y_coordinate, line)
        y_coordinate += SIZE_DOWN_TEXT

    canvas.showPage()
    canvas.save()
    buffer.seek(0)

    return buffer
