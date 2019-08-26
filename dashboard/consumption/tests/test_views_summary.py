from __future__ import unicode_literals

import json

from django.urls import resolve, reverse

from .base import BaseTestCase
from ..views import SummaryView


class SummaryViewTestCase(BaseTestCase):

    def test_url_resolve(self):
        found = resolve(reverse('summary'))
        self.assertEqual(found.func.__name__, SummaryView.as_view().__name__)

    def test_list_summary(self):
        response = self.client.get(reverse('summary'))
        self.assertEqual(200, response.status_code)

        self.assertIn('title', response.context_data)
        self.assertIn('users', response.context_data)
        self.assertIn('chart', response.context_data)

        # title
        self.assertEqual('Summary', response.context_data['title'])

        # chart
        chart = json.loads(response.context_data['chart'])
        self.assertIn('type', chart)
        self.assertIn('data', chart)
        self.assertIn('options', chart)

        data = chart['data']
        self.assertTrue('datasets' in data)
        self.assertEqual(list, type(data['datasets']))
        self.assertTrue('labels' in data)
        self.assertEqual(list, type(data['labels']))

        dataset = data['datasets'][0]
        self.assertIn('label', dataset)
        self.assertIn('data', dataset)
