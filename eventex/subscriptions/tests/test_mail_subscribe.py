from django.core import mail
from django.conf import settings

from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Arthur Dent', cpf='01234567890',
                    email='arthur@dent.uk', phone='21-99999-9999')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expected = 'Confirmação de inscrição'
        self.assertEqual(expected, self.email.subject)

    def test_subscription_email_from(self):
        expected = settings.DEFAULT_FROM_EMAIL
        self.assertEqual(expected, self.email.from_email)

    def test_subscription_email_to(self):
        expected = [settings.DEFAULT_FROM_EMAIL, 'arthur@dent.uk']
        self.assertEqual(expected, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Arthur Dent',
            '01234567890',
            'arthur@dent.uk',
            '21-99999-9999'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
