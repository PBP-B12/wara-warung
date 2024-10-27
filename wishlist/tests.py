from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Wishlist, Category, Menu

class WishlistViewTest(TestCase):

    def setUp(self):
        # Create a test user and log them in
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create some test data
        self.category = Category.objects.create(name="Test Category", user=self.user)
        self.menu_item = Menu.objects.create(menu="Test Menu", harga=10000, gambar="test.jpg")
        self.wishlist_item = Wishlist.objects.create(user=self.user, menu=self.menu_item)
    
    def test_wishlist_view_status_code(self):
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)

    def test_wishlist_uses_correct_template(self):
        response = self.client.get(reverse('wishlist'))
        self.assertTemplateUsed(response, 'wishlist.html')

    def test_nonexistent_page(self):
        response = self.client.get('/nonexistent_page/')
        self.assertEqual(response.status_code, 404)

    def test_add_category_ajax(self):
        response = self.client.post(
            reverse('add_category'),
            {'name': 'New Category'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('New Category', [cat['name'] for cat in response.json()['categories']])

    def test_remove_from_wishlist_ajax(self):
        response = self.client.post(
            reverse('remove_from_wishlist', args=[self.menu_item.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_assign_category_to_item_ajax(self):
        new_category = Category.objects.create(name="Assigned Category", user=self.user)
        response = self.client.post(
            reverse('assign_category_to_item', args=[self.wishlist_item.id]),
            {'category_id': new_category.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.wishlist_item.refresh_from_db()
        self.assertEqual(self.wishlist_item.categories.first().name, "Assigned Category")
