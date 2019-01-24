# coding=utf-8
from __future__ import division, print_function, unicode_literals

from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Band(models.Model):
    name = models.CharField(max_length=20)
    nr_of_members = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name
