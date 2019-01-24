# coding=utf-8
from __future__ import division, print_function, unicode_literals

from distutils.version import LooseVersion

import django
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from django.utils.html import strip_spaces_between_tags

from .admin import BandAdmin
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


@override_settings(ROOT_URLCONF="tests.admin_changelist.urls")
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

    def setUp(self):
        self.client.force_login(self.superuser)

    def _mocked_authenticated_request(self, url, user):
        request = self.factory.get(url)
        request.user = user
        return request

    def _test_aggregations_django1(self):
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
        if LooseVersion(django.__version__) < LooseVersion('2'):
            self._test_aggregations_django1()
        else:
            self._test_aggregations_django2()

    def _test_template_django1(self):
        response = self.client.get(reverse('admin:admin_changelist_band_changelist'))
        content_row1_html = '''
            <tr class="row1">
            <td class="action-checkbox">
            <input type="checkbox" name="_selected_action" value="1" class="action-select" />
            </td>
            <th class="field-name">
            <a href="/admin/admin_changelist/band/1/change/">Pink Floyd</a>
            </th>
            <td class="field-nr_of_members">5</td>
            <td class="field-_genres">Progressive rock, Psychedelic rock</td>
            </tr>
        '''
        content_row2_html = '''
            <tr class="row2">
            <td class="action-checkbox">
            <input type="checkbox" name="_selected_action" value="2" class="action-select" />
            </td>
            <th class="field-name">
            <a href="/admin/admin_changelist/band/2/change/">Blondie</a>
            </th>
            <td class="field-nr_of_members">6</td>
            <td class="field-_genres">New wave, Pop rock, Punk rock</td>
            </tr>
        '''
        totals_row_html = '''
            <tr>
            <th>
              <b style="padding: 8px;"></b>
            </th>
            <th>
              <b style="padding: 8px;"></b>
            </th>
            <th>
              <b style="padding: 8px;">5.5</b>
            </th>
            <th>
              <b style="padding: 8px;">5</b>
            </th>
            </tr>
        '''
        response_html = strip_spaces_between_tags(response.rendered_content)
        for expected_element_html in [
            content_row1_html,
            content_row2_html,
            totals_row_html
        ]:
            expected_element_html = strip_spaces_between_tags(expected_element_html).strip()
            self.assertNotEqual(
                response_html.find(expected_element_html),
                -1,
                'Failed to find expected row element: %s' % expected_element_html)

    def _test_template_django2(self):
        response = self.client.get(reverse('admin:admin_changelist_band_changelist'))
        content_row1_html = '''
            <tr class="row1">
            <td class="action-checkbox">
            <input type="checkbox" name="_selected_action" value="1" class="action-select">
            </td>
            <th class="field-name">
            <a href="/admin/admin_changelist/band/1/change/">Pink Floyd</a>
            </th>
            <td class="field-nr_of_members">5</td>
            <td class="field-_genres">Progressive rock, Psychedelic rock</td>
            </tr>
        '''
        content_row2_html = '''
            <tr class="row2">
            <td class="action-checkbox">
            <input type="checkbox" name="_selected_action" value="2" class="action-select">
            </td>
            <th class="field-name">
            <a href="/admin/admin_changelist/band/2/change/">Blondie</a>
            </th>
            <td class="field-nr_of_members">6</td>
            <td class="field-_genres">New wave, Pop rock, Punk rock</td>
            </tr>
        '''
        totals_row_html = '''
            <tr>
            <th>
              <b style="padding: 8px;"></b>
            </th>
            <th>
              <b style="padding: 8px;"></b>
            </th>
            <th>
              <b style="padding: 8px;">5.5</b>
            </th>
            <th>
              <b style="padding: 8px;">5</b>
            </th>
            </tr>
        '''
        response_html = strip_spaces_between_tags(response.rendered_content)
        for expected_element_html in [
            content_row1_html,
            content_row2_html,
            totals_row_html
        ]:
            expected_element_html = strip_spaces_between_tags(expected_element_html).strip()
            self.assertNotEqual(
                response_html.find(expected_element_html),
                -1,
                'Failed to find expected row element: %s' % expected_element_html)

    def test_template(self):
        if LooseVersion(django.__version__) < LooseVersion('2.1'):
            # Django 2.0 passes only with this test
            self._test_template_django1()
        else:
            self._test_template_django2()
