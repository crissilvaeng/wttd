from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.subscription = Subscription.objects.create(name='Arthur Dent', cpf='01234567890',
                                                        email='arthur@dent.uk', phone='21-99999-9999')
        self.response = self.client.get(f'/inscricao/{self.subscription.pk}/')

    def test_get(self):
        """GET /inscricao/1/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'detail.html')

    def test_context(self):
        self.assertIsInstance(self.response.context['subscription'], Subscription)

    def test_html(self):
        contents = (self.subscription.name, self.subscription.cpf, self.subscription.email, self.subscription.phone,)
        for content in contents:
            with self.subTest():
                self.assertContains(self.response, content)
