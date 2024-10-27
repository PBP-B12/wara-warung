from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserEntry

class userDashboardTest(TestCase):
    
    #create test user
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='testuser@gmail.com', 
            password='password123'
        )
        self.profile = UserEntry.objects.create(
            user=self.user,
            phone_number='1234567890',
            address='123 Depok',
            date_of_birth='1990-01-01'
        )
        self.client = Client()

    #test apakah user bisa mengakses dashboard
    def test_dashboard_url_is_exist(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_dashboard:show_user_dashboard'))
        self.assertEqual(response.status_code, 200)

    #test apakah dashboard menggunakan template yang benar
    def test_dashboard_using_dashboard_template(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_dashboard:show_user_dashboard'))
        self.assertTemplateUsed(response, 'user_dashboard.html')
    
    #test apakah data user terisi dengan benar di awal sebelum di edit
    def test_profile_data_prefill(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_dashboard:show_user_dashboard'))
        self.assertContains(response, 'testuser@gmail.com')

    #test apakah user bisa mengedit profile
    def test_edit_profile_post(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('user_dashboard:edit_user', args=[self.profile.id]), {
            'phone_number': '0987654321',
            'address': '456 Depok',
            'date_of_birth': '1985-05-05'
        })
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_number, '0987654321')
        self.assertEqual(self.profile.address, '456 Depok')
        self.assertEqual(str(self.profile.date_of_birth), '1985-05-05')

    #test apakah user akan log out secara automatis setelah delete account
    def test_logout_after_delete_account(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('user_dashboard:delete_user_account'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json()['status'])

        response = self.client.get(reverse('user_dashboard:show_user_dashboard'))
        self.assertNotEqual(response.status_code, 200) 
    
