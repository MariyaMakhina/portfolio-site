from django.test import TestCase
from wagtail.models import Page

class BlogTestCase(TestCase):
    def test_home_page_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_portfolio_page_exists(self):
        response = self.client.get('/photo_studio/portfolio_photo/')
        self.assertEqual(response.status_code, 200)
    
    def test_about_page_exists(self):
        response = self.client.get('/photo_studio/about_photo/')
        self.assertEqual(response.status_code, 200)
    
    def test_contact_page_exists(self):
        response = self.client.get('/contact_photo/')
        self.assertEqual(response.status_code, 200)