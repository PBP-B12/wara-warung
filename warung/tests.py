from django.test import TestCase
from django.urls import reverse
from warung.models import Warung
from menu.models import Menu
from ratereview.models import Review
from django.contrib.auth.models import User
from django.db.models import Avg

class WarungAppTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create test Warung entries
        self.warung1 = Warung.objects.create(nama="Warung A", alamat="Alamat A", telepon=123456)
        self.warung2 = Warung.objects.create(nama="Warung B", alamat="Alamat B", telepon=789012)
        
        # Create test Menu entries linked to the warungs
        self.menu1 = Menu.objects.create(warung="Warung A", menu="Menu A1", harga=15000, gambar="gambar_a1.jpg")
        self.menu2 = Menu.objects.create(warung="Warung A", menu="Menu A2", harga=20000, gambar="gambar_a2.jpg")
        self.menu3 = Menu.objects.create(warung="Warung B", menu="Menu B1", harga=25000, gambar="gambar_b1.jpg")
        
        # Create test Reviews
        Review.objects.create(menu=self.menu1, user=self.user, rating=3)
        Review.objects.create(menu=self.menu2, user=self.user, rating=4)
        Review.objects.create(menu=self.menu3, user=self.user, rating=5)

    def test_show_main_view(self):
        # Test the main warung list view
        response = self.client.get(reverse('warung:show_main'))
        
        # Check if response status is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Verify that the view uses the correct template
        self.assertTemplateUsed(response, 'allwarung.html')
        
        # Check if all Warung entries are passed in context
        expected_warungs = list(Warung.objects.all())
        actual_warungs = list(response.context['warung_entries'])
        self.assertEqual(expected_warungs, actual_warungs)

    def test_show_warung_view(self):
        # Test the detail view for a specific Warung
        response = self.client.get(reverse('warung:show_warung', args=["Warung A"]))
        
        # Check if response status is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Verify that the view uses the correct template
        self.assertTemplateUsed(response, 'warung.html')
        
        # Check if specific Warung entries are passed in context
        expected_warungs = list(Warung.objects.filter(nama="Warung A"))
        actual_warungs = list(response.context['warung_entries'])
        self.assertEqual(expected_warungs, actual_warungs)
        
        # Check if menus associated with "Warung A" and their avg_ratings are in the context
        expected_menus_with_avg = [
            {
                'menu': self.menu1,
                'avg_rating': Review.objects.filter(menu=self.menu1).aggregate(Avg('rating'))['rating__avg'] or 0
            },
            {
                'menu': self.menu2,
                'avg_rating': Review.objects.filter(menu=self.menu2).aggregate(Avg('rating'))['rating__avg'] or 0
            }
        ]
        actual_menus_with_avg = list(response.context['menu_entries'])
        
        # Convert each menu's avg_rating to float for comparison
        for menu in actual_menus_with_avg:
            menu['avg_rating'] = float(menu['avg_rating'])
        
        self.assertEqual(expected_menus_with_avg, actual_menus_with_avg)
