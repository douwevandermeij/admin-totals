# coding=utf-8
from __future__ import division, print_function, unicode_literals

from django.contrib.admin.templatetags.admin_list import (result_headers,
                                                          result_hidden_fields,
                                                          results)
from django.template import Library

register = Library()


@register.inclusion_tag("admin_totals/change_list_results_totals.html")
def result_list_totals(cl):
    """
    Displays the headers, totals bar and data list together
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': list(results(cl))}
