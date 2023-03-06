import json
import os

from django.db import migrations
from api_foodgram.settings import BASE_DIR


def create_ingredients(apps, schema_editor):
    Model = apps.get_model('recipes', 'Ingredient')
    with open(os.path.join(BASE_DIR, 'data/ingredients.json'), 'r') as data:
        ingredients = json.load(data)
        Model.objects.bulk_create(
            [Model(
                name=ingredient['name'].capitalize(),
                measurement_unit=ingredient['measurement_unit'].lower()
                ) for ingredient in ingredients]
        )


def create_tags(apps, schema_editor):
    Model = apps.get_model('recipes', 'Tag')
    with open(os.path.join(BASE_DIR, 'data/tags.json'), 'r') as data:
        ingredients = json.load(data)
        Model.objects.bulk_create(
            [Model(**tag) for tag in ingredients]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_ingredient_name'),
    ]

    operations = [
        migrations.RunPython(create_ingredients),
        migrations.RunPython(create_tags)

    ]
