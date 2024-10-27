from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from menu.models import Menu
from ratereview.models import Review

class RateReviewAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.menu = Menu.objects.create(menu="Sample Menu", harga=10000, warung="Sample Warung", gambar="sample.jpg")

        self.menu_detail_url = reverse('ratereview:menu_detail', args=[self.menu.id])
        self.submit_review_url = reverse('ratereview:submit_review', args=[self.menu.id])

    def test_menu_detail_view(self):
        response = self.client.get(self.menu_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu_detail.html')
        self.assertEqual(response.context['reviews'].count(), 0)
        self.assertEqual(response.context['avg_rating'], 0)

    def test_submit_review_ajax(self):
        # Initial GET request to set the CSRF token
        self.client.get(self.menu_detail_url)
        
        # Retrieve CSRF token from client cookies
        csrf_token = self.client.cookies['csrftoken'].value
        
        # Test valid review submission with AJAX
        response = self.client.post(self.submit_review_url, {
            'rating': 5,
            'comment': "Amazing taste!",
            'csrfmiddlewaretoken': csrf_token
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(int(response_data['review']['rating']), 5)  # Convert to int
        self.assertEqual(response_data['review']['comment'], "Amazing taste!")
        self.assertEqual(response_data['review']['user'], self.user.username)