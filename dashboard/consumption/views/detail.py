from __future__ import unicode_literals

import json

from django.db.models import Avg
from django.views.generic import TemplateView

from .mixins import ConsumptionViewMixin
from ..models import User


class DetailView(ConsumptionViewMixin, TemplateView):
    template_name = 'consumption/detail.html'

    def get_chart_data(self, queryset):
        data = queryset.filter(user_id=self.kwargs['user_id'])
        averages = queryset.values('datetime').annotate(avg=Avg('consumption'))

        return {
            'datasets': [{
                'label': 'Consumption details',
                'data': [d.consumption for d in data],
                'borderColor': "rgba(54,164,235,0.8)",
                'backgroundColor': "rgba(54,164,235,0.5)",
                'yAxisID': 'y-axis-detail',
            }, {
                'label': 'Consumptions average',
                'type': 'line',
                'fill': False,
                'data': [a['avg'] for a in averages],
                'backgroundColor': "rgba(255, 99, 132, 0.8)",
                'borderColor': "rgba(255, 99, 132, 0.5)",
                'yAxisID': 'y-axis-average',
            }],
            'labels': [d.datetime.strftime('%Y-%m-%d %H:%M') for d in data],
        }

    def get_chart_options(self):
        return {
            'responsive': True,
            'scales': {
                'xAxes': [{
                    'ticks': {
                        'autoSkip': True,
                        'maxTicksLimit': 20,
                    },
                }],
                'yAxes': [{
                    'id': 'y-axis-detail',
                    'type': 'linear',
                    'position': 'left',
                    'ticks': {
                        'suggestedMax': 10000,
                        'suggestedMin': 0,
                        'maxTicksLimit': 10,
                    },
                }, {
                    'id': 'y-axis-average',
                    'type': 'linear',
                    'position': 'right',
                    'ticks': {
                        'suggestedMax': 10000,
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

    def get_context_data(self, **kwargs):
        queryset = super().get_queryset()
        user = User.objects.get(id=kwargs['user_id'])
        context = {
            'title': 'Detail',
            'user': user,
            'values': queryset.filter(user_id=kwargs['user_id']),
            'chart': json.dumps(self.get_chart_content(queryset)),
        }
        return context
