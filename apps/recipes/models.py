from django.contrib.auth import get_user_model
from django.db import models
from .validation import validate_zero

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=256, verbose_name="name")
    dimension = models.CharField(max_length=256, verbose_name="unit")

    class Meta:
        ordering = ("title",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=("title", "dimension"), name="unique_composition_link"
            ),
        ]

    def __str__(self):
        return f"{self.title}, {self.dimension}"


class Recipe(models.Model):
    title = models.CharField(max_length=256, verbose_name="name")
    author = models.ForeignKey(
        User,
        related_name="recipes",
        on_delete=models.CASCADE,
        verbose_name="author",
    )
    text = models.TextField(verbose_name="text")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="pub date")
    cooking_time = models.PositiveIntegerField(
        verbose_name="Cooking time", validators=[validate_zero]
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient", verbose_name="ingredients"
    )
    tags = models.ManyToManyField(
        "Tag", blank=True, related_name="recipes", verbose_name="tags"
    )
    image = models.ImageField(
        blank=False, upload_to="recipes/", verbose_name="image"
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f"{self.title}"


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="ingredient"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="recipe"
    )
    quantity = models.PositiveIntegerField(verbose_name="value")

    class Meta:
        verbose_name = "Ингредиенты рецепта"
        verbose_name_plural = "Ингредиенты рецептов"


class TagChoices(models.TextChoices):
    BREAKFAST = "breakfast", "Завтрак"
    LUNCH = "lunch", "Обед"
    DINNER = "dinner", "Ужин"


class ColorChoices(models.TextChoices):
    GREEN = "green", "Зеленый"
    ORANGE = "orange", "Оранжевый"
    PURPLE = "purple", "Фиолетовый"


class Tag(models.Model):
    title = models.CharField(
        choices=TagChoices.choices,
        default=TagChoices.LUNCH,
        unique=True,
        max_length=10,
        verbose_name="title",
    )
    color = models.CharField(
        choices=ColorChoices.choices,
        default=ColorChoices.GREEN,
        unique=True,
        max_length=10,
        verbose_name="color",
    )

    class Meta:
        ordering = ("pk",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.title


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="in_favorites",
        verbose_name="recipe",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_recipes",
        verbose_name="user",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("recipe", "user"), name="unique_favorite_recipe"
            )
        ]
        verbose_name = "Избранный"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f"{self.recipe.title} is {self.user.username} favorite"


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="user",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="in_purchases",
        verbose_name="recipe",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_purchase"
            ),
        ]
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"

    def __str__(self):
        return f"{self.user}, {self.recipe}"
