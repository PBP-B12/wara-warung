from django.test import TestCase, Client
from django.urls import reverse
from menu.models import Menu

class SearchMenuViewTests(TestCase):
    def setUp(self):
        # Create sample menu items for testing
        Menu.objects.create(menu="Nasi Goreng", harga=15000, warung="Warung A", gambar="image1.jpg")
        Menu.objects.create(menu="Mie Ayam", harga=10000, warung="Warung B", gambar="image2.jpg")
        Menu.objects.create(menu="Sate Ayam", harga=25000, warung="Warung C", gambar="image3.jpg")
        self.client = Client()
    
    def test_search_view_without_ajax(self):
        """Test rendering of search.html when the request is not AJAX."""
        response = self.client.get(reverse('search:search_menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_search_view_ajax_query(self):
        """Test AJAX request with a query filter."""
        response = self.client.get(
            reverse('search:search_menu'),
            {'query': 'Nasi'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())
        # Check if the filtered result contains the expected menu
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['menu'], 'Nasi Goreng')
    
    def test_search_view_ajax_budget_filter(self):
        """Test AJAX request with a budget filter."""
        response = self.client.get(
            reverse('search:search_menu'),
            {'budget': 20000},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())
        # Only items under 20000 should appear
        self.assertEqual(len(response.json()['results']), 2)
        self.assertNotIn('Sate Ayam', [item['menu'] for item in response.json()['results']])
    
    def test_search_view_ajax_query_and_budget(self):
        """Test AJAX request with both query and budget filters."""
        response = self.client.get(
            reverse('search:search_menu'),
            {'query': 'Mie', 'budget': 20000},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())
        # Only "Mie Ayam" should match both filters
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['menu'], 'Mie Ayam')
