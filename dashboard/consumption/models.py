from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.utils.timezone import utc


class User(models.Model):
    id = models.IntegerField(
        'User ID',
        primary_key=True,
    )
    area = models.CharField('Area', max_length=2)
    tariff = models.CharField('Tariff', max_length=2)

    def __str__(self):
        return f'{self.id}'


class ConsumptionManager(models.Manager):
    def get_exist_dates(self):
        # return Consumption.objects \
        #     .values('datetime') \
        #     .distinct() \
        #     .datetimes('datetime', 'day')
        return [datetime(2016, 7, 15, tzinfo=utc)]


class Consumption(models.Model):
    id = models.IntegerField(
        'ID',
        primary_key=True,
        auto_created=True,
    )
    user = models.ForeignKey(
        User,
        related_name='consumptions',
        on_delete=models.PROTECT,
    )
    datetime = models.DateTimeField('Datetime')
    consumption = models.FloatField('Consumption amount per half hour')

    objects = ConsumptionManager()

    def __str__(self):
        return f'{self.datetime} <{self.consumption}>'

    class Meta:
        ordering = (
            'datetime',
        )
