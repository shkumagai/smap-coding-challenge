from django.db.models import ProtectedError

from .base import BaseTestCase
from ..models import User


class UserTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.user4 = User(id=4030, area='t1', tariff='t1')
        self.user4.save()

    def test_get(self):
        records = User.objects.all()
        self.assertEqual(4, len(records))

        record = User.objects.filter(id=4000)
        self.assertEqual(1, len(record))

    def test_add(self):
        user = User()
        user.id = 5000
        user.area = 'a5'
        user.tariff = 't5'
        user.save()

        datum = User.objects.get(id=5000)
        self.assertEqual(5000, datum.id)
        self.assertEqual('a5', datum.area)
        self.assertEqual('t5', datum.tariff)

    def test_update(self):
        before = User.objects.get(id=4020)
        self.assertEqual('t3', before.tariff)
        before_value = before.tariff

        before.tariff = 't5'
        before.save()

        after = User.objects.get(id=4020)
        self.assertNotEqual(before_value, after.tariff)

    def test_delete(self):
        before = User.objects.get(id=4030)
        self.assertTrue(before)

        User.objects.filter(id=4030).delete()

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=4030)

    def test_cannot_delete_user_who_has_consumptions(self):
        before = User.objects.get(id=4020)
        self.assertTrue(before)

        with self.assertRaises(ProtectedError):
            User.objects.filter(id=4020).delete()
