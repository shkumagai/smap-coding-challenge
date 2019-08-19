# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from statistics import median

from django.db.models import Avg, Max, Min, Sum
from django.views.generic import TemplateView

from .mixins import ConsumptionViewMixin

# Create your views here.


class SummaryView(ConsumptionViewMixin, TemplateView):
    template_name = 'consumption/summary.html'

    def get_queryset(self):
        return super().get_queryset()

    def get_users(self, queryset):
        return queryset.values('user_id', 'user__area', 'user__tariff') \
            .annotate(
                sum=Sum('consumption'),
                max=Max('consumption'),
                min=Min('consumption'),
                avg=Avg('consumption')) \
            .order_by('user_id')

    def get_chart_data(self, queryset):
        data = queryset.values('datetime') \
            .annotate(
                sum=Sum('consumption'),
                avg=Avg('consumption')) \
            .order_by('datetime')

        stats = {}
        for c in queryset.order_by('datetime'):
            key = c.datetime.strftime('%Y-%m-%d %H:%M:%S')
            values = stats.setdefault(key, [])
            stats[key] = values + [c.consumption]

        return {
            'datasets': [{
                'label': 'Total consumptions',
                'data': [d['sum'] for d in data],
                'borderColor': "rgba(54,164,235,0.8)",
                'backgroundColor': "rgba(54,164,235,0.5)",
                'yAxisID': 'y-axis-total',
            }, {
                'label': 'Consumptions median',
                'type': 'line',
                'data': [median(v) for v in stats.values()],
                'backgroundColor': "rgba(255, 99, 132, 0.8)",
                'borderColor': "rgba(255, 99, 132, 0.5)",
                'yAxisID': 'y-axis-average',
            }],
            'labels': [d['datetime'].strftime('%Y-%m-%d %H:%M') for d in data],
        }

    def get_chart_options(self):
        return {
            'responsive': True,
            'scales': {
                'xAxes': [{
                    'ticks': {
                        'autoSkip': True,
                        'maxTicksLimit': 20,
                    }
                }],
                'yAxes': [{
                    'id': 'y-axis-total',
                    'type': 'linear',
                    'position': 'left',
                    'ticks': {
                        'suggestedMax': 30000,
                        'suggestedMin': 0,
                        'maxTicksLimit': 10,
                    },
                }, {
                    'id': 'y-axis-average',
                    'type': 'linear',
                    'position': 'right',
                    'ticks': {
                        'suggestedMax': 1200,
                        'suggestedMin': 0,
                        'maxTicksLimit': 10,
                    },
                }],
            },
        }

    def get_chart_content(self, queryset):
        return {
            'type': 'bar',
            'data': self.get_chart_data(queryset),
            'options': self.get_chart_options(),
        }

    def get_context_data(self):
        queryset = self.get_queryset()
        context = {
            'title': 'Summary',
            'users': self.get_users(queryset),
            'chart': json.dumps(self.get_chart_content(queryset)),
        }
        return context
