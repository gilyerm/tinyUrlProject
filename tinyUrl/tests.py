import json

from django.test import TestCase


class TinyUrlTestCase(TestCase):
    def test_create(self):
        response = self.client.post('/create', json.dumps({'url': 'https://www.google.com'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('short_url' in response.json())
        self.assertEqual(len(response.json()['short_url']), 7)

    def test_redirect(self):
        response = self.client.post('/create', json.dumps({'url': 'https://www.google.com'}),
                                    content_type='application/json')
        short_url = response.json()['short_url']
        response = self.client.get(f'/s/{short_url}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://www.google.com')

    def test_create_invalid_method(self):
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 405)
        self.assertTrue('error' in response.json())

    def test_create_no_url(self):
        response = self.client.post('/create', json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def test_create_invalid_content_type(self):
        response = self.client.post('/create', 'url=https://www.google.com', content_type='text/plain')
        self.assertEqual(response.status_code, 415)
        self.assertTrue('error' in response.json())

    def test_create_invalid_json(self):
        response = self.client.post('/create', 'invalid json', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def test_create_invalid_url(self):
        response = self.client.post('/create', json.dumps({'url': 123}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def test_create_existing_url(self):
        response = self.client.post('/create', json.dumps({'url': 'https://www.google.com'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/create', json.dumps({'url': 'https://www.google.com'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('short_url' in response.json())

    def test_redirect_no_short_url(self):
        response = self.client.get('/s/')
        self.assertEqual(response.status_code, 404)
        self.assertTrue('error' in response.json())

    def test_redirect_not_found_short_url(self):
        response = self.client.get('/s/abcde12345')
        self.assertEqual(response.status_code, 404)
        self.assertTrue('error' in response.json())
