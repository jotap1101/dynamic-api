import os
import random
import sys
from datetime import datetime, timedelta
from decimal import Decimal

import django
from faker import Faker

# Configurar ambiente Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Importar modelos
from apps.app1.models import Category, Product
from apps.app2.models import Animal, Breed, Species
from apps.app3.models import Genre, Movie

# Inicializar Faker
fake = Faker()


def populate_app1():
    """Popula o banco de dados db1 com categorias e produtos"""
    print("Populando banco de dados db1...")

    # Criar categorias
    categories = []
    category_names = [
        "Eletrônicos",
        "Roupas",
        "Alimentos",
        "Livros",
        "Casa e Decoração",
    ]
    for name in category_names:
        category = Category.objects.using("db1").create(
            name=name, description=fake.paragraph()
        )
        categories.append(category)

    # Criar produtos
    for _ in range(20):
        Product.objects.using("db1").create(
            name=fake.unique.catch_phrase(),  # Usando catch_phrase para nomes de produtos únicos
            description=fake.paragraph(),
            price=Decimal(str(random.uniform(10.0, 1000.0))).quantize(Decimal("0.01")),
            category=random.choice(categories),
        )

    print("Banco de dados db1 populado com sucesso!")


def populate_app2():
    """Popula o banco de dados db2 com espécies, raças e animais"""
    print("Populando banco de dados db2...")

    # Criar espécies
    species = []
    species_names = ["Cachorro", "Gato", "Pássaro", "Peixe", "Réptil"]
    for name in species_names:
        species_obj = Species.objects.using("db2").create(
            name=name, description=fake.text()
        )
        species.append(species_obj)

    # Criar raças
    breeds = []
    for sp in species:
        for _ in range(3):
            breed = Breed.objects.using("db2").create(
                name=fake.unique.first_name(), species=sp, description=fake.text()
            )
            breeds.append(breed)

    # Criar animais
    for _ in range(30):
        Animal.objects.using("db2").create(
            name=fake.first_name(),
            age=random.randint(1, 15),
            breed=random.choice(breeds),
            description=fake.text(),
        )

    print("Banco de dados db2 populado com sucesso!")


def populate_app3():
    """Popula o banco de dados db3 com gêneros e filmes"""
    print("Populando banco de dados db3...")

    # Criar gêneros
    genres = []
    genre_names = ["Ação", "Comédia", "Drama", "Ficção Científica", "Terror", "Romance"]
    for name in genre_names:
        genre = Genre.objects.using("db3").create(name=name, description=fake.text())
        genres.append(genre)

    # Criar filmes
    for _ in range(25):
        Movie.objects.using("db3").create(
            title=fake.unique.catch_phrase(),
            description=fake.text(),
            release_date=fake.date_between(start_date="-30y", end_date="today"),
            genre=random.choice(genres),
        )

    print("Banco de dados db3 populado com sucesso!")


if __name__ == "__main__":
    # Limpar registros existentes
    print("Limpando bancos de dados...")

    # Limpar db1
    Product.objects.using("db1").all().delete()
    Category.objects.using("db1").all().delete()

    # Limpar db2
    Animal.objects.using("db2").all().delete()
    Breed.objects.using("db2").all().delete()
    Species.objects.using("db2").all().delete()

    # Limpar db3
    Movie.objects.using("db3").all().delete()
    Genre.objects.using("db3").all().delete()

    # Popular bancos de dados
    populate_app1()
    populate_app2()
    populate_app3()

    print("\nTodos os bancos de dados foram populados com sucesso!")
