from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.app1.models import Category, Product
from apps.app2.models import Animal, Breed, Species
from apps.app3.models import Genre, Movie
from apps.auth.models import User


class DynamicAPITestCase(APITestCase):
    """Base test case with common setup and helper methods."""

    # Define quais bancos de dados podem ser acessados pelos testes
    databases = {"default", "db1", "db2", "db3"}

    def setUp(self):
        """Set up test data and authentication."""
        # Create test user and get JWT token
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
        )

        # Create test data in each database
        self.setup_app1_data()
        self.setup_app2_data()
        self.setup_app3_data()

    def setup_app1_data(self):
        """Set up test data for app1 (db1)."""
        self.category = Category.objects.using("db1").create(
            name="Test Category", description="Test Description"
        )
        category_id = self.category.id  # Store the UUID
        self.category = Category.objects.using("db1").get(
            id=category_id
        )  # Refresh from DB
        self.product = Product.objects.using("db1").create(
            name="Test Product",
            description="Test Description",
            price=99.99,
            category=self.category,
        )

    def setup_app2_data(self):
        """Set up test data for app2 (db2)."""
        self.species = Species.objects.using("db2").create(
            name="Test Species", description="Test Description"
        )
        self.breed = Breed.objects.using("db2").create(
            name="Test Breed", description="Test Description", species=self.species
        )
        self.animal = Animal.objects.using("db2").create(
            name="Test Animal", age=5, description="Test Description", breed=self.breed
        )

    def setup_app3_data(self):
        """Set up test data for app3 (db3)."""
        self.genre = Genre.objects.using("db3").create(
            name="Test Genre", description="Test Description"
        )
        self.movie = Movie.objects.using("db3").create(
            title="Test Movie",
            description="Test Description",
            release_date="2025-01-01",
            genre=self.genre,
        )

    def get_dynamic_url(self, database, model, pk=None):
        """Helper method to generate dynamic API URLs."""
        if pk:
            return reverse(
                "dynamic-detail",
                kwargs={"database": database, "model": model, "id": pk},
            )
        return reverse("dynamic-list", kwargs={"database": database, "model": model})


class AuthenticationTests(DynamicAPITestCase):
    """Test authentication requirements."""

    def test_access_without_token(self):
        """Test that endpoints require authentication."""
        # Remove authentication credentials
        self.client.credentials()

        # Test different endpoints
        urls = [
            self.get_dynamic_url("db1", "product"),
            self.get_dynamic_url("db2", "animal"),
            self.get_dynamic_url("db3", "movie"),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_invalid_token(self):
        """Test that invalid tokens are rejected."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")

        url = self.get_dynamic_url("db1", "product")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CRUDTests(DynamicAPITestCase):
    """Test CRUD operations for each database."""

    def test_list_objects(self):
        """Test listing objects from different databases."""
        # Test db1 (products)
        response = self.client.get(self.get_dynamic_url("db1", "product"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["count"], 1)

        # Test db2 (animals)
        response = self.client.get(self.get_dynamic_url("db2", "animal"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["count"], 1)

        # Test db3 (movies)
        response = self.client.get(self.get_dynamic_url("db3", "movie"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["count"], 1)

    def test_create_objects(self):
        """Test creating objects in different databases."""
        # Test creating product in db1
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 149.99,
            "category": self.category.id,  # Send UUID directly
        }
        response = self.client.post(
            self.get_dynamic_url("db1", "product"), product_data, format="json"
        )
        if response.status_code != status.HTTP_201_CREATED:
            print("Product creation error:", response.data)  # Debug info
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test creating animal in db2
        animal_data = {
            "name": "New Animal",
            "age": 3,
            "description": "New Description",
            "breed": self.breed.id,  # Send UUID directly
        }
        response = self.client.post(
            self.get_dynamic_url("db2", "animal"), animal_data, format="json"
        )
        if response.status_code != status.HTTP_201_CREATED:
            print("Animal creation error:", response.data)  # Debug info
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test creating movie in db3
        movie_data = {
            "title": "New Movie",
            "description": "New Description",
            "release_date": "2025-02-01",
            "genre": self.genre.id,  # Send UUID directly
        }
        response = self.client.post(
            self.get_dynamic_url("db3", "movie"), movie_data, format="json"
        )
        if response.status_code != status.HTTP_201_CREATED:
            print("Movie creation error:", response.data)  # Debug info
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_objects(self):
        """Test retrieving specific objects from different databases."""
        # Test retrieving product from db1
        response = self.client.get(
            self.get_dynamic_url("db1", "product", str(self.product.id))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Product")

        # Test retrieving animal from db2
        response = self.client.get(
            self.get_dynamic_url("db2", "animal", str(self.animal.id))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Animal")

        # Test retrieving movie from db3
        response = self.client.get(
            self.get_dynamic_url("db3", "movie", str(self.movie.id))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Movie")

    def test_update_objects(self):
        """Test updating objects in different databases."""
        # Test updating product in db1
        product_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 199.99,
            "category": self.category.id,  # Send UUID directly
        }
        response = self.client.put(
            self.get_dynamic_url("db1", "product", str(self.product.id)),
            product_data,
            format="json",
        )
        if response.status_code != status.HTTP_200_OK:
            print("Product update error:", response.data)  # Debug info
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Product")

    def test_delete_objects(self):
        """Test deleting objects from different databases."""
        # Test deleting product from db1
        response = self.client.delete(
            self.get_dynamic_url("db1", "product", str(self.product.id))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify deletion
        response = self.client.get(
            self.get_dynamic_url("db1", "product", str(self.product.id))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ErrorHandlingTests(DynamicAPITestCase):
    """Test error handling scenarios."""

    def test_invalid_database(self):
        """Test accessing an invalid database."""
        response = self.client.get(self.get_dynamic_url("invalid_db", "product"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_model(self):
        """Test accessing an invalid model."""
        response = self.client.get(self.get_dynamic_url("db1", "invalid_model"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_object_id(self):
        """Test accessing an invalid object ID."""
        response = self.client.get(
            self.get_dynamic_url(
                "db1", "product", "00000000-0000-0000-0000-000000000000"
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_data_creation(self):
        """Test creating objects with invalid data."""
        # Test with missing required fields
        response = self.client.post(
            self.get_dynamic_url("db1", "product"), {"description": "Only Description"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test with invalid field value
        response = self.client.post(
            self.get_dynamic_url("db2", "animal"),
            {
                "name": "Invalid Animal",
                "age": "not a number",  # age should be integer
                "breed": str(self.breed.id),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
