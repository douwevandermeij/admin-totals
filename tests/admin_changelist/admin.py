# coding=utf-8
from __future__ import division, print_function, unicode_literals

from django.contrib import admin
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce

from admin_totals.admin import ModelAdminTotals

from .models import Band

site = admin.AdminSite(name="admin")


class BandAdmin(ModelAdminTotals):
    list_display = ['name', 'nr_of_members', '_genres']
    list_totals = [
        ('nr_of_members', Avg),
        ('_genres', lambda field: Coalesce(Count('genres'), 0))
    ]
    ordering = ('nr_of_members',)

    def _genres(self, band):
        return ', '.join(str(g) for g in band.genres.all())


site.register(Band, BandAdmin)
