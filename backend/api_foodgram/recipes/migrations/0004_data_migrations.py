import json
import os

from django.conf import settings
from django.db import migrations


def create_ingredients(apps, schema_editor):
    Model = apps.get_model('recipes', 'Ingredient')
    with open(os.path.join(settings.BASE_DIR, 'data/ingredients.json'), 'r',
              encoding='UTF-8') as data:
        ingredients = json.load(data)
        Model.objects.bulk_create(
            [Model(
                name=ingredient['name'].lower(),
                measurement_unit=ingredient['measurement_unit'].lower()
                ) for ingredient in ingredients]
        )


def create_tags(apps, schema_editor):
    Model = apps.get_model('recipes', 'Tag')
    with open(os.path.join(settings.BASE_DIR, 'data/tags.json'), 'r',
              encoding='UTF-8') as data:
        tags = json.load(data)
        Model.objects.bulk_create(
            [Model(**tag) for tag in tags]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('recipes',
         '0003_alter_favorite_options_alter_shoppingcart_options_and_more'),
    ]

    operations = [
        migrations.RunPython(create_ingredients),
        migrations.RunPython(create_tags)

    ]
