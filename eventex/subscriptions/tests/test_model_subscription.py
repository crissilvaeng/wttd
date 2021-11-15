from datetime import datetime
from uuid import UUID

from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(name='Arthur Dent', cpf='01234567890',
                                email='arthur@dent.uk', phone='21-99999-9999')
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Arthur Dent', str(self.obj))

    def test_has_uuid(self):
        self.assertIsNotNone(self.obj.uuid)
