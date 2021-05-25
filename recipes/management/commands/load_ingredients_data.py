import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'load ingredients data to database'

    def handle(self, *args, **options):
        with open('recipes/fixtures/ingredients.csv', encoding='utf8') as file:
            reader = csv.reader(file)
            for row in reader:
                title, dimension = row
                Ingredient.objects.get_or_create(
                    title=title,
                    dimension=dimension,
                )
