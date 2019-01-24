# Django Admin Totals

Module to show totals in Django Admin List.

[![codecov](https://codecov.io/gh/douwevandermeij/admin-totals/branch/master/graph/badge.svg)](https://codecov.io/gh/douwevandermeij/admin-totals)
[![Build Status](https://travis-ci.org/douwevandermeij/admin-totals.svg?branch=master)](https://travis-ci.org/douwevandermeij/admin-totals)

## Installation

    virtualenv .
    source bin/activate
    pip install git+https://github.com/douwevandermeij/admin-totals.git

## Usage

In settings.py

    INSTALLED_APPS = [
        'admin_totals',
    ]

In admin.py:

    from admin_totals.admin import ModelAdminTotals
    from django.contrib import admin
    from django.db.models import Sum, Avg
    from django.db.models.functions import Coalesce

    @admin.register(MyModel)
    class MyModelAdmin(ModelAdminTotals):
        list_display = ['col_a', 'col_b', 'col_c']
        list_totals = [('col_b', lambda field: Coalesce(Sum(field), 0))), ('col_c', Avg)]

Make sure to at least have the columns of `list_totals` in `list_display`.

## Tests

    python runtests.py
