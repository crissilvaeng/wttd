import shortuuid

from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(name='Arthur Dent', cpf='01234567890',
                                               email='arthur@dent.uk', phone='21-99999-9999')
        id = shortuuid.encode(self.obj.uuid)
        self.response = self.client.get(f'/inscricao/{id}/')

    def test_get(self):
        """GET /inscricao/<id>/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use detail.html"""
        self.assertTemplateUsed(self.response, 'detail.html')

    def test_context(self):
        """Context must have subscription"""
        self.assertIsInstance(self.response.context['subscription'], Subscription)

    def test_html(self):
        """Must contain subscription's data"""
        contents = (self.obj.name, self.obj.cpf, self.obj.email, self.obj.phone,)
        for content in contents:
            with self.subTest():
                self.assertContains(self.response, content)


class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        """Must return status code 404"""
        response = self.client.get('/inscricao/0/')
        self.assertEqual(404, response.status_code)
