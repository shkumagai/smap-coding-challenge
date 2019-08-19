from __future__ import unicode_literals

import random
from datetime import datetime, timedelta

from django.test import TestCase
from django.utils.timezone import utc

from consumption.models import Consumption, User


class BaseTestCase(TestCase):

    def setUp(self):
        self.user1 = User(id=4000, area='a1', tariff='t1')
        self.user1.save()
        self.user2 = User(id=4010, area='a2', tariff='t2')
        self.user2.save()
        self.user3 = User(id=4020, area='a3', tariff='t3')
        self.user3.save()

        entries = []
        self.basedate = datetime(2016, 7, 15, 0, 0).astimezone(utc)

        for n in range(48):
            for u in [self.user1, self.user2, self.user3]:
                entries.append(
                    Consumption(
                        datetime=self.basedate + timedelta(minutes=n * 30),
                        consumption=random.random() * n * 30,
                        user=u,
                    ),
                )
        Consumption.objects.bulk_create(entries)
