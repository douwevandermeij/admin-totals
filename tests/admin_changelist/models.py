from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=20)


class Band(models.Model):
    name = models.CharField(max_length=20)
    nr_of_members = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre)
