# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.utils.timezone import utc

from ..models import Consumption

# Create your views here.


class ConsumptionViewMixin:
    model = Consumption

    def get_queryparams(self):
        value = self.request.GET.get('date')
        if value is None:
            date = Consumption.objects.get_exist_dates()[0]
        else:
            try:
                date = datetime.strptime(value, '%Y-%m-%d').astimezone(utc)
            except RuntimeError:
                date = Consumption.objects.get_exist_dates()[0]
        return date

    def get_queryset(self):
        date = self.get_queryparams()
        return self.model.objects.filter(
            datetime__gte=date,
            datetime__lt=date + timedelta(days=1),
        )
