# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.urls import reverse, resolve

from .base import BaseTestCase
from ..views import DetailView

# Create your tests here.


class DetailViewTestCase(BaseTestCase):

    def test_url_resolve(self):
        found = resolve(reverse('detail', kwargs={'user_id': 4000}))
        self.assertEqual(found.func.__name__, DetailView.as_view().__name__)

    def test_list_detail(self):
        response = self.client.get(reverse('detail', kwargs={'user_id': 4000}))
        self.assertEqual(200, response.status_code)

        self.assertIn('title', response.context_data)
        self.assertIn('user', response.context_data)
        self.assertIn('values', response.context_data)
        self.assertIn('chart', response.context_data)

        # title
        self.assertEqual('Detail', response.context_data['title'])

        # user
        self.assertEqual(4000, response.context_data['user'].id)
        self.assertEqual('a1', response.context_data['user'].area)
        self.assertEqual('t1', response.context_data['user'].tariff)

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
