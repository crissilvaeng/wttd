from django.core import mail
from django.conf import settings

from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscribe.html"""
        self.assertTemplateUsed(self.response, 'subscribe.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def tet_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.response.context['form']
        self.assertSequenceEqual(
            ['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Arthur Dent', cpf='01234567890',
                    email='arthur@dent.uk', phone='21-99999-9999')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expected = 'Confirmação de inscrição'
        self.assertEqual(expected, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expected = settings.EMAIL_SENDER
        self.assertEqual(expected, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expected = [settings.EMAIL_SENDER, 'arthur@dent.uk']
        self.assertEqual(expected, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]
        contents = [
            'Arthur Dent',
            '01234567890',
            'arthur@dent.uk',
            '21-99999-9999'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, email.body)


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscribe.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        data = dict(name='Arthur Dent', cpf='01234567890',
                    email='arthur@dent.uk', phone='21-99999-9999')
        self.response = self.client.post('/inscricao/', data, follow=True)

    def test_message(self):
        self.assertContains(self.response, 'Inscrição realizada com sucesso!')
