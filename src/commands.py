from flask.cli import with_appcontext
import click

from src.ext import db
from src.models import Plant, Question
import random

@click.command("init_db")
@with_appcontext
def init_db():
    click.echo('Initializing database')
    db.drop_all()
    db.create_all()
    click.echo('Database initialized')

@click.command("populate_db")
@with_appcontext
def populate_db():
    click.echo('Populating database')
    click.echo('Creating tables')

    with db.session.begin():
        db.session.add_all(gen_sample())

    click.echo('Sample plants have been created')



def gen_sample():
    plant_names = [
        "Aloe Vera", "Bamboo Palm", "Cactus", "Daisy", "Eucalyptus", "Fern", "Gardenia",
        "Hibiscus", "Ivy", "Jasmine", "Kalanchoe", "Lavender", "Marigold", "Nasturtium",
        "Orchid", "Peony", "Quince", "Rosemary", "Sunflower", "Tulip", "Umbrella Plant",
        "Verbena", "Willow", "Xerophyte", "Yucca", "Zinnia", "Acacia", "Begonia", "Camellia",
        "Dracaena", "Echeveria", "Freesia", "Gladiolus", "Honeysuckle", "Iris", "Juniper",
        "Knotweed", "Lily", "Mimosa", "Nerium", "Oleander", "Pansy", "Quaking Grass", "Rhododendron",
        "Sage", "Thyme", "Uva Ursi", "Violet", "Wisteria", "Xylosma", "Yarrow", "Zephyranthes"
    ]
    plants = []
    used_names = set()

    for _ in range(50):
        # Ensure unique names
        name = random.choice(plant_names)
        while name in used_names:
            name = random.choice(plant_names)
        used_names.add(name)

        eng_name = name
        lat_name = f"{name[::-1]}"
        image = f"{name.replace(' ', '_').lower()}_image.jpg"

        plant = Plant(
            name=name,
            eng_name=eng_name,
            lat_name=lat_name,
            image=image
        )
        plants.append(plant)

    return plants