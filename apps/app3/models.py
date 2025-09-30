from django.db import models
from uuid import uuid4

# Create your models here.
class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField()
    genre = models.ForeignKey(
        Genre, related_name="movies", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title