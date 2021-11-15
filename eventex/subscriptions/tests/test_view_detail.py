from django.test import TestCase


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/1/')

    def test_get(self):
        """GET /inscricao/1/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)
