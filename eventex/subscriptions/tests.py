from django.test import TestCase


class SubscriptionTest(TestCase):
    def setUp(self) -> None:
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
                ('<input', 5),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)
