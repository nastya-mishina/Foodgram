import csv
import os

from django.core.management.base import BaseCommand

from apps.recipes.models import Ingredient
from foodgram.settings import BASE_DIR

CSV_FILE_PATH = os.path.join(BASE_DIR, "ingredients.csv")


class Command(BaseCommand):
    help = "Load ingredient"

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH, encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                name, unit = row
                Ingredient.objects.get_or_create(title=name, dimension=unit)
