# coding=utf-8
from __future__ import print_function, unicode_literals, division

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList


class ChangeListTotals(ChangeList):
    def get_results(self, *args, **kwargs):
        super(ChangeListTotals, self).get_results(*args, **kwargs)
        if hasattr(self.model_admin, 'list_totals'):
            self.aggregations = []
            list_totals = dict(self.model_admin.list_totals)
            for field in self.list_display:
                if field in list_totals:
                    self.aggregations.append(self.result_list.aggregate(agg=list_totals[field](field))['agg'] or 0)
                else:
                    self.aggregations.append('')


class ModelAdminTotals(admin.ModelAdmin):
    change_list_template = 'admin_tools/change_list_totals.html'

    def get_changelist(self, request, **kwargs):
        return ChangeListTotals
