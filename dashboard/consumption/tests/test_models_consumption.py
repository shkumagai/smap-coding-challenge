from datetime import datetime

from .base import BaseTestCase
from ..models import Consumption


class ConsumptionModelTestCase(BaseTestCase):
    def test_get(self):
        records = Consumption.objects.all()
        self.assertEqual(48 * 3, len(records))

        records = Consumption.objects.filter(user=self.user1)
        self.assertEqual(48, len(records))

    def test_add(self):
        record = Consumption()
        record.datetime = datetime.strptime('2018-08-19 00:00:00+0000', '%Y-%m-%d %H:%M:%S%z')
        record.consumption = 999.0
        record.user = self.user1
        record.save()

        datum = Consumption.objects.get(user=self.user1, datetime='2018-08-19 00:00:00+0000')

        self.assertEqual(datum.datetime, record.datetime)
        self.assertEqual(datum.consumption, record.consumption)
        self.assertEqual(datum.user, record.user)

    def test_update(self):
        before = Consumption.objects.get(user=self.user3, datetime=self.basedate)
        self.assertTrue(before)
        before_value = before.consumption

        before.consumption = 9999.0
        before.save()

        after = Consumption.objects.get(user=self.user3, datetime=self.basedate)
        self.assertNotEqual(before_value, after.consumption)

    def test_delete(self):
        before = Consumption.objects.get(user=self.user3, datetime=self.basedate)
        self.assertTrue(before)

        Consumption.objects.filter(user=self.user3, datetime=self.basedate).delete()

        with self.assertRaises(Consumption.DoesNotExist):
            Consumption.objects.get(user=self.user3, datetime=self.basedate)
