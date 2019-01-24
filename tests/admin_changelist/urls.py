# coding=utf-8
from __future__ import division, print_function, unicode_literals

from django.conf.urls import url

from . import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
