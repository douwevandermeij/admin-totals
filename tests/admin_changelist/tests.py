import django
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce
from django.test import TestCase
from django.test.client import RequestFactory

from admin_totals.admin import ModelAdminTotals

from .admin import site as custom_site
from .models import Band

# Test code based on Django's own test code: django/tests/admin_changelist/tests.py


def get_changelist_args(modeladmin, **kwargs):
    m = modeladmin
    args = (
        kwargs.pop('list_display', m.list_display),
        kwargs.pop('list_display_links', m.list_display_links),
        kwargs.pop('list_filter', m.list_filter),
        kwargs.pop('date_hierarchy', m.date_hierarchy),
        kwargs.pop('search_fields', m.search_fields),
        kwargs.pop('list_select_related', m.list_select_related),
        kwargs.pop('list_per_page', m.list_per_page),
        kwargs.pop('list_max_show_all', m.list_max_show_all),
        kwargs.pop('list_editable', m.list_editable),
        m,
    )
    assert not kwargs, "Unexpected kwarg %s" % kwargs
    return args


class ChangeListTests(TestCase):
    factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username='super', email='a@b.com', password='xxx')
        pink_floyd = Band.objects.create(name='Pink Floyd', nr_of_members=5)
        pink_floyd.genres.create(name='Progressive rock')
        pink_floyd.genres.create(name='Psychedelic rock')
        blondie = Band.objects.create(name='Blondie', nr_of_members=6)
        blondie.genres.create(name='New wave')
        blondie.genres.create(name='Pop rock')
        blondie.genres.create(name='Punk rock')

    def _mocked_authenticated_request(self, url, user):
        request = self.factory.get(url)
        request.user = user
        return request

    def _test_aggregations_django1(self):
        class BandAdmin(ModelAdminTotals):
            list_display = ['name', 'nr_of_members', 'genres']
            list_totals = [
                ('nr_of_members', Avg),
                ('genres', lambda field: Coalesce(Count('genres'), 0))
            ]
            ordering = ('nr_of_members')

        band_admin = BandAdmin(Band, custom_site)
        request = self._mocked_authenticated_request('/band/', self.superuser)
        ChangeList = band_admin.get_changelist(request)
        cl = ChangeList(request, Band, *get_changelist_args(band_admin))
        cl.get_results(request)
        self.assertEqual(
            cl.aggregations,
            [
                '',
                5.5,
                5
            ]
        )

    def _test_aggregations_django2(self):
        class BandAdmin(ModelAdminTotals):
            list_display = ['name', 'nr_of_members', 'genres']
            list_totals = [
                ('nr_of_members', Avg),
                ('genres', lambda field: Coalesce(Count('genres'), 0))
            ]
            ordering = ('nr_of_members')

        band_admin = BandAdmin(Band, custom_site)
        request = self._mocked_authenticated_request('/band/', self.superuser)
        cl = band_admin.get_changelist_instance(request)
        cl.get_results(request)
        self.assertEqual(
            cl.aggregations,
            [
                '',
                '',
                5.5,
                5
            ]
        )

    def test_aggregations(self):
        if django.__version__.startswith('1'):
            self._test_aggregations_django1()
        else:
            self._test_aggregations_django2()
