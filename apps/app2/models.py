from django.db import models
from uuid import uuid4


# Create your models here.
class Species(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Breed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    species = models.ForeignKey(
        Species, related_name="breeds", on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Animal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    breed = models.ForeignKey(
        Breed, related_name="animals", on_delete=models.SET_NULL, null=True
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
