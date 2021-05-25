from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название')
    color_tags = models.CharField(max_length=20, verbose_name='Цвет')
    style = models.CharField(max_length=20, unique=True, verbose_name='Вид')

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента',
    )
    dimension = models.CharField(max_length=20, verbose_name='Количество')

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название рецепта')
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(
        Ingredient,
        through="Ingredients_recipe",
        through_fields=('recipe', 'ingredient'),
    )
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    text = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_author',
        verbose_name='Автор рецепта',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']


class Ingredients_recipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
    )
    units = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.ingredient.dimension


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_user",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite_recipe",
    )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buyer",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_list",
    )
